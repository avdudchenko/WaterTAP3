.. _ammonia_addition_unit:

Ammonia Addition
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

The ammonia solution flow `S` [gal/day] is used in a cost curve of the general form:

    .. math::

        C = a S ^ b
|
For a ammonia addition unit, `a` = 6699.1 and `b` = 0.4219. The full cost equation in
WaterTAP3 is:

    .. math::

        C_{amm} = 6699.1 S ^ {0.4219}
|
This cost is then multiplied by the number of units and the EIF factor for the final FCI for the
chemical addition. These parameters were determined by fitting data from Figure 5.5.11 in McGivney & Kawamura (2008).

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

        M_{amm} = Q_{in} D_{amm}
|
* The volumetric flow `S` [gal/min] of the chemical solution, which incorporates the solution
  density [kg/m3] and ratio of the chemical in the solution [v/v]:

    .. math::

        S = \frac{M_{amm}}{\rho_{amm} X_{amm}}
|
* The pump and motor efficiencies:

    .. math::

        \eta_{pump}, \eta_{motor}
|
Then the electricity intensity is calculated as [kWh/m3]:

    .. math::

        E_{amm} = \frac{0.746 S h}{3960 \eta_{pump} \eta_{motor} Q_{in}}
|

Assumptions
------------------------

* Number of units = 2
* Solution density [kg/m3] = 1360
* Ratio in solution = 0.5
* Lift height [ft] = 100
* Pump efficiency = 0.9
* Motor efficiency = 0.9


Reference
------------------------

| William McGivney & Susumu Kawamura (2008)
| Cost Estimating Manual for Water Treatment Facilities
| DOI:10.1002/9780470260036

Ammonia Addition Module
----------------------------------------

.. autoclass:: watertap3.wt_units.ammonia_addition.UnitProcess
   :members: fixed_cap, elect, get_costing, solution_vol_flow
   :undoc-members: build
   :exclude-members: build


..  raw:: pdf

    PageBreak