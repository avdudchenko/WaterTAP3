from pyomo.environ import Block, Expression, units as pyunits
from watertap3.utils import financials
from watertap3.wt_units.wt_unit import WT3UnitProcess

## REFERENCE: ADD REFERENCE HERE

module_name = 'irwin_brine_management'
basis_year = 2019
tpec_or_tic = 'TPEC'


class UnitProcess(WT3UnitProcess):

    def fixed_cap(self):
        time = self.flowsheet().config.time.first()
        self.flow_in = pyunits.convert(self.flow_vol_in[time], to_units=pyunits.m ** 3 / pyunits.hr)
        self.conc_mass_tot = 0
        for constituent in self.config.property_package.component_list:
            self.conc_mass_tot += self.conc_mass_in[time, constituent]
        self.density = 0.6312 * self.conc_mass_tot + 997.86
        self.total_mass = self.density * self.flow_in
        self.chem_dict = {}
        self.capacity_basis = 9463.5
        self.base_fixed_cap_cost = 31
        self.cap_scaling_exp = 0.873
        irwin_bm_cap = self.base_fixed_cap_cost * (self.total_mass / self.capacity_basis) ** self.cap_scaling_exp
        return irwin_bm_cap

    def elect(self):
        self.lift_height = 100 * pyunits.ft
        self.pump_eff = 0.9 * pyunits.dimensionless
        self.motor_eff = 0.9 * pyunits.dimensionless
        flow_in_gpm = pyunits.convert(self.flow_in, to_units=pyunits.gallons / pyunits.minute)
        electricity = (0.746 * flow_in_gpm * self.lift_height / (3960 * self.pump_eff * self.motor_eff)) / self.flow_in
        return electricity

    def get_costing(self, unit_params=None, year=None):
        '''
        Initialize the unit in WaterTAP3.
        '''
        financials.create_costing_block(self, basis_year, tpec_or_tic)
        self.costing.fixed_cap_inv_unadjusted = Expression(expr=self.fixed_cap(),
                                                           doc='Unadjusted fixed capital investment')
        self.electricity = Expression(expr=self.elect(),
                                      doc='Electricity intensity [kwh/m3]')
        financials.get_complete_costing(self.costing)