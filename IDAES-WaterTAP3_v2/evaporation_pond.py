##############################################################################
# Institute for the Design of Advanced Energy Systems Process Systems
# Engineering Framework (IDAES PSE Framework) Copyright (c) 2018-2020, by the
# software owners: The Regents of the University of California, through
# Lawrence Berkeley National Laboratory,  National Technology & Engineering
# Solutions of Sandia, LLC, Carnegie Mellon University, West Virginia
# University Research Corporation, et al. All rights reserved.
#
# Please see the files COPYRIGHT.txt and LICENSE.txt for full copyright and
# license information, respectively. Both files are also available online
# at the URL "https://github.com/IDAES/idaes-pse".
##############################################################################
"""
Demonstration zeroth-order model for WaterTAP3
"""

# Import IDAES cores
from idaes.core import (declare_process_block_class, UnitModelBlockData, useDefault)
from idaes.core.util.config import is_physical_parameter_block
# Import Pyomo libraries
from pyomo.common.config import ConfigBlock, ConfigValue, In

# Import WaterTAP# financials module
import financials
from financials import *  # ARIEL ADDED
import numpy as np
from scipy.optimize import curve_fit
# Import properties and units from "WaterTAP Library"
from pyomo.environ import *
from cost_curves import evap_ratio_curve
##########################################
####### UNIT PARAMETERS ######
# At this point (outside the unit), we define the unit parameters that do not change across case studies or analyses ######.
# Below (in the unit), we define the parameters that we may want to change across case studies or analyses. Those parameters should be set as variables (eventually) and atttributed to the unit model (i.e. m.fs.UNIT_NAME.PARAMETERNAME). Anything specific to the costing only should be in  m.fs.UNIT_NAME.costing.PARAMETERNAME ######
##########################################

## REFERENCE: Cost Estimating Manual for Water Treatment Facilities (McGivney/Kawamura)

### MODULE NAME ###
module_name = "evaporation_pond"

# Cost assumptions for the unit, based on the method #
# this is either cost curve or equation. if cost curve then reads in data from file.
unit_cost_method = "cost_curve"
tpec_or_tic = "TPEC"
unit_basis_yr = 2007


# You don't really want to know what this decorator does
# Suffice to say it automates a lot of Pyomo boilerplate for you
@declare_process_block_class("UnitProcess")
class UnitProcessData(UnitModelBlockData):
    """
    This class describes the rules for a zeroth-order model for a unit

    The Config Block is used tpo process arguments from when the model is
    instantiated. In IDAES, this serves two purposes:
         1. Allows us to separate physical properties from unit models
         2. Lets us give users options for configuring complex units
    The dynamic and has_holdup options are expected arguments which must exist
    The property package arguments let us define different sets of contaminants
    without needing to write a new model.
    """

    CONFIG = ConfigBlock()
    CONFIG.declare("dynamic", ConfigValue(domain=In([False]), default=False, description="Dynamic model flag - must be False", doc="""Indicates whether this model will be dynamic or not,
**default** = False. Equilibrium Reactors do not support dynamic behavior."""))
    CONFIG.declare("has_holdup", ConfigValue(default=False, domain=In([False]), description="Holdup construction flag - must be False", doc="""Indicates whether holdup terms should be constructed or not.
**default** - False. Equilibrium reactors do not have defined volume, thus
this must be False."""))
    CONFIG.declare("property_package", ConfigValue(default=useDefault, domain=is_physical_parameter_block, description="Property package to use for control volume", doc="""Property parameter object used to define property calculations,
**default** - useDefault.
**Valid values:** {
**useDefault** - use default package from parent model or flowsheet,
**PhysicalParameterObject** - a PhysicalParameterBlock object.}"""))
    CONFIG.declare("property_package_args", ConfigBlock(implicit=True, description="Arguments to use for constructing property packages", doc="""A ConfigBlock with arguments to be passed to a property block(s)
and used when constructing these,
**default** - None.
**Valid values:** {
see property package for documentation.}"""))

    def build(self):
        import unit_process_equations
        return unit_process_equations.build_up(self, up_name_test=module_name)

    # NOTE ---> THIS SHOULD EVENTUaLLY BE JUST FOR COSTING INFO/EQUATIONS/FUNCTIONS. EVERYTHING ELSE IN ABOVE.
    def get_costing(self, module=financials, cost_method="wt", year=None, unit_params=None):
        """
        We need a get_costing method here to provide a point to call the
        costing methods, but we call out to an external consting module
        for the actual calculations. This lets us easily swap in different
        methods if needed.

        Within IDAES, the year argument is used to set the initial value for
        the cost index when we build the model.
        """
        # First, check to see if global costing module is in place
        # Construct it if not present and pass year argument
        if not hasattr(self.flowsheet(), "costing"):
            self.flowsheet().get_costing(module=module, year=year)

        # Next, add a sub-Block to the unit model to hold the cost calculations
        # This is to let us separate costs from model equations when solving
        self.costing = Block()
        # Then call the appropriate costing function out of the costing module
        # The first argument is the Block in which to build the equations
        # Can pass additional arguments as needed

        ##########################################
        ####### UNIT SPECIFIC VARIABLES AND CONSTANTS -> SET AS SELF OTHERWISE LEAVE AT TOP OF FILE ######
        ##########################################

        ### COSTING COMPONENTS SHOULD BE SET AS SELF.costing AND READ FROM A .CSV THROUGH A FUNCTION THAT SITS IN FINANCIALS ###

        time = self.flowsheet().config.time.first()
        # get tic or tpec (could still be made more efficent code-wise, but could enough for now)
        sys_cost_params = self.parent_block().costing_param
        self.costing.tpec_tic = sys_cost_params.tpec if tpec_or_tic == "TPEC" else sys_cost_params.tic
        tpec_tic = self.costing.tpec_tic

        # basis year for the unit model - based on reference for the method.
        self.costing.basis_year = unit_basis_yr

        #### CHEMS ###
        tds_in = self.conc_mass_in[time, "tds"]  # convert from kg/m3 to mg/L

        chem_dict = {}
        self.chem_dict = chem_dict
        ##########################################
        ####### UNIT SPECIFIC EQUATIONS AND FUNCTIONS ######
        ##########################################
        approach = unit_params['approach']


        try:
            evap_method = unit_params['evap_method']
        except:
            evap_method = False
        try:
            self.humidity = unit_params['humidity'] # ratio, e.g. 50% humidity = 0.5
            self.wind_speed = unit_params['wind_speed'] # m / s
        except:
            self.humidity = 0.5 # ratio, e.g. 50% humidity = 0.5
            self.wind_speed = 5 # m / s

        if bool(evap_method):
            evap_method = unit_params['evap_method']
            try:
                self.air_temp = unit_params['air_temp']  # degree C
                self.solar_rad  = unit_params['solar_rad']  # mJ / m2
            except:
                self.air_temp = 25
                self.solar_rad  = 25 # average for 40deg latitude
            if evap_method == 'turc':
                # Turc (1961) PE in mm for day
                self.evap_rate_pure = (0.313 * self.air_temp * (self.solar_rad  + 2.1) / (self.air_temp + 15)) * (pyunits.millimeter / pyunits.day)
                self.evap_rate_pure = pyunits.convert(self.evap_rate_pure, to_units=(pyunits.gallons / pyunits.minute / pyunits.acre))


            if evap_method == 'jensen':
                # Jensen-Haise (1963) PE in mm per day
                self.evap_rate_pure = (0.41 * (0.025 * self.air_temp + 0.078) * self.solar_rad ) * (pyunits.millimeter / pyunits.day)
                self.evap_rate_pure = pyunits.convert(self.evap_rate_pure, to_units=(pyunits.gallons / pyunits.minute / pyunits.acre))
        else:
            # defaults to turc
            self.air_temp = 25
            self.solar_rad = 25  # average for 40deg latitude
            self.evap_rate_pure = (0.313 * self.air_temp * (self.solar_rad  + 2.1) / (self.air_temp + 15)) * (pyunits.millimeter / pyunits.day)
            self.evap_rate_pure = pyunits.convert(self.evap_rate_pure, to_units=(pyunits.gallons / pyunits.minute / pyunits.acre))

        x0 = self.air_temp
        x1 = tds_in
        x2 = self.humidity
        x3 = self.wind_speed
        self.ratio = -0.0465233559 * (x0) - 0.0011189096 * (x1) - 0.7088094852 * (x2) - 0.0257883428 * (x3) + 0.0017209498 * (x0 ** 2) + 7.54344e-05 * (x0 * x1) + 0.0923261483 * (x0 * x2) - 0.0002522583 * (
                x0 * x3) + 7.74e-07 * (x1 ** 2) + 0.0012751516 * (x1 * x2) + 1.16276e-05 * (x1 * x3) - 0.042838386 * (x2 ** 2) + 0.0842127857 * (x2 * x3) + 0.0006828725 * (x3 ** 2) - 2.55508e-05 * (
                       x0 ** 3) - 1.6415e-06 * (x0 ** 2 * x1) - 0.001500322 * (x0 ** 2 * x2) + 4.46853e-05 * (x0 ** 2 * x3) + 2.8e-08 * (x0 * x1 ** 2) - 8.93471e-05 * (x0 * x1 * x2) - 2.6285e-06 * (
                       x0 * x1 * x3) - 0.0472354101 * (x0 * x2 ** 2) + 0.000814877 * (x0 * x2 * x3) - 0.0001268287 * (x0 * x3 ** 2) - 2.4e-09 * (x1 ** 3) + 1.9905e-06 * (x1 ** 2 * x2) - 1.214e-07 * (
                       x1 ** 2 * x3) - 0.0004983631 * (x1 * x2 ** 2) - 0.0002213007 * (x1 * x2 * x3) + 1.36134e-05 * (x1 * x3 ** 2) + 0.4822279076 * (x2 ** 3) - 0.0473877989 * (
                       x2 ** 2 * x3) - 0.0027941016 * (x2 * x3 ** 2) + 9.36662e-05 * (x3 ** 3) + 1.3159327466



        self.evap_rate = self.evap_rate_pure * self.ratio

        flow_in = pyunits.convert(self.flow_vol_in[time], to_units=(pyunits.gallons / pyunits.minute))

        self.area = (flow_in / self.evap_rate_pure)

        def fixed_cap(approach, flow_in):
            if approach == 'zld':
                return 0.3 * self.area
            else:
                return 0.03099 * pyunits.convert(flow_in, to_units=(pyunits.m ** 3 / pyunits.day)) ** 0.7613



        # Get the first time point in the time domain
        # In many cases this will be the only point (steady-state), but lets be
        # safe and use a general approach

        ## fixed_cap_inv_unadjusted ##
        self.costing.fixed_cap_inv_unadjusted = Expression(
            expr=fixed_cap(approach, flow_in),
            doc="Unadjusted fixed capital investment")  # $M

        ## electricity consumption ##
        self.electricity = 0  # kwh/m3

        ##########################################
        ####### GET REST OF UNIT COSTS ######
        ##########################################

        module.get_complete_costing(self.costing)
