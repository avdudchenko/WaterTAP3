.. _hydrochloric_acid_addition_unit:

Hydrochloric Acid Addition
=====================================

Costs for chemical additions are based on the chemical dose required to treat the water and the inlet flow to the unit.

Unit Parameters
--------------------

There is one unit parameter:

* ``"dose"`` - dose of chemical [mg/L]

    * Required parameter
|
Capital Costs
---------------

The hydrochloric acid solution flow `S` [gal/day] is used in a cost curve of the general form:

    .. math::

        C = a S ^ b
|
For a single hydrochloric acid addition unit, `a` = 900.97 and `b` = 0.6179. The full cost
equation in WaterTAP3 is:

    .. math::

        C_{HCl} = 900.97 S ^ {0.6179}
|
This cost is then multiplied by the number of units and the EIF factor for the final FCI for the
chemical addition. These parameters were determined by fitting data from FIGURE 5.5.11 - SULFURIC
ACID FEED in McGivney & Kawamura (2008).


Electricity Intensity
------------------------

Electricity intensity for chemical additions is based off the pump used to inject
the chemical solution, the chemical solution flow rate, and the influent flow rate. The
calculation includes:

* Lift height [ft]:

    .. math::

        h
|
* The mass flow rate [kg/day] of the solution necessary to achieve the desired dose:

    .. math::

        M_{HCl} = Q_{in} D_{HCl}
|
* The volumetric flow `S` [gal/min] of the chemical solution, which incorporates the solution
  density [kg/m3]:

    .. math::

        S = \frac{M_{HCl}}{\rho_{HCl}}
|
* The pump and motor efficiencies:

    .. math::

        \eta_{pump}, \eta_{motor}
|
Then the electricity intensity is calculated as [kWh/m3]:

    .. math::

        E_{HCl} = \frac{0.746 S h}{3960 \eta_{pump} \eta_{motor} Q_{in}}
|

Assumptions
------------------------

* Number of units = 2
* Solution density [kg/m3] = 1490
* Lift height [ft] = 100
* Pump efficiency = 0.9
* Motor efficiency = 0.9

Reference
------------------------

| William McGivney & Susumu Kawamura (2008)
| Cost Estimating Manual for Water Treatment Facilities
| DOI:10.1002/9780470260036

Hydrochloric Acid Addition Module
----------------------------------------

.. autoclass:: watertap3.wt_units.hydrochloric_acid_addition.UnitProcess
   :members: fixed_cap, elect, get_costing, solution_vol_flow
   :undoc-members: build
   :exclude-members: build


..  raw:: pdf

    PageBreak