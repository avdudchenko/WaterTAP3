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

##########################################
####### UNIT PARAMETERS ######
# At this point (outside the unit), we define the unit parameters that do not change across case studies or analyses ######.
# Below (in the unit), we define the parameters that we may want to change across case studies or analyses. Those parameters should be set as variables (eventually) and atttributed to the unit model (i.e. m.fs.UNIT_NAME.PARAMETERNAME). Anything specific to the costing only should be in  m.fs.UNIT_NAME.costing.PARAMETERNAME ######
##########################################

## REFERENCE: Cost Estimating Manual for Water Treatment Facilities (McGivney/Kawamura)

### MODULE NAME ###
module_name = "water_pumping_station"

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
		flow_in = pyunits.convert(self.flow_vol_in[time], to_units=pyunits.gallon / pyunits.minute)  # m3 /hr
		# get tic or tpec (could still be made more efficent code-wise, but could enough for now)
		sys_cost_params = self.parent_block().costing_param
		self.costing.tpec_tic = sys_cost_params.tpec if tpec_or_tic == "TPEC" else sys_cost_params.tic
		tpec_tic = self.costing.tpec_tic

		# basis year for the unit model - based on reference for the method.
		self.costing.basis_year = unit_basis_yr

		def power_curve(x, a, b):
			return a * x ** b

		# TODO -->> ADD THESE TO UNIT self.X
		pump_type = unit_params['pump_type']
		tdh = unit_params['tdh'] * pyunits.ft

		if pump_type == 'raw':
			flow_lst = np.array([10, 19, 53, 79, 105, 132, 159, 185, 200])  # mgd
			flow_cost = np.array([188032, 303010, 726314, 1050344, 1363933, 1677539, 1991145, 2299522, 2482431])  # $
			cc, _ = curve_fit(power_curve, flow_lst, flow_cost)
			a, b = cc[0], cc[1]

		if pump_type == 'treated':
			flow_lst = np.array([53, 80, 106, 131, 158, 185, 211, 238, 265, 300])  # mgd
			flow_cost = np.array([1254215, 1775451, 2271801, 2755748, 3239590, 3711029, 4107735, 4616463, 5025624, 5633425])  # $
			cc, _ = curve_fit(power_curve, flow_lst, flow_cost)
			a, b = cc[0], cc[1]

		motor_eff = 0.9
		pump_eff = 0.9
		tdh_lst = [25, 50, 75, 100, 200, 300, 400, 1000, 2500]  # TDH in ft
		# tdh_elect = [*map(lambda x: (0.746 * value(flow_in) * x) / (3960 * motor_eff * pump_eff), tdh_lst)]
		tdh_elect = [(0.746 * 440.29 * x) / (3960 * motor_eff * pump_eff) for x in tdh_lst]
		cc, _ = curve_fit(power_curve, tdh_lst, tdh_elect)
		c, d = cc[0], cc[1]
		#### CHEMS ###

		chem_dict = {}
		self.chem_dict = chem_dict

		##########################################
		####### UNIT SPECIFIC EQUATIONS AND FUNCTIONS ######
		##########################################

		def fixed_cap(flow_in):
			flow_in_cap = pyunits.convert(flow_in, to_units=(pyunits.Mgallons / pyunits.day))
			if pump_type == 'raw':
				return tpec_tic * a * flow_in_cap ** b * 1E-6  # $MM
			if pump_type == 'treated':
				return tpec_tic * a * flow_in_cap ** b * 1E-6

		def electricity(flow_in):  # m3/hr
			flow_in_elect = pyunits.convert(flow_in, to_units=(pyunits.Mgallons / pyunits.day))
			electricity = (c * (flow_in_elect / 440.29) ** d) / flow_in # kWh / m3
			return electricity

		# Get the first time point in the time domain
		# In many cases this will be the only point (steady-state), but lets be
		# safe and use a general approach

		## fixed_cap_inv_unadjusted ##
		self.costing.fixed_cap_inv_unadjusted = Expression(expr=fixed_cap(flow_in), doc="Unadjusted fixed capital investment")  # $M

		## electricity consumption ##
		self.electricity = electricity(flow_in)  # kwh/m3

		##########################################
		####### GET REST OF UNIT COSTS ######
		##########################################

		module.get_complete_costing(self.costing)
