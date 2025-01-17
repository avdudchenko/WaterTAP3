.. _cartridge_filtration_unit:

Cartridge Filtration
============================================================

Unit Parameters
--------------------

None

Capital Costs
---------------

The capital costs are a function of flow [MGD] with cost curve parameters from McGivney &
Kawamura (2008):

    .. math::

        C_{cart} = 0.72557 Q_{in} ^ {0.5862}
|
Electricity Intensity
------------------------

Electricity intensity for cartridge filtration is fixed at 2E-4 kWh/m3 and is taken from Bukhary,
et al. (2019).

References
-------------

CAPITAL
**********

| William McGivney & Susumu Kawamura (2008)
| Cost Estimating Manual for Water Treatment Facilities
| DOI:10.1002/9780470260036

ELECTRICITY
**************

| Bukhary, S., Batista, J., Ahmad, S. (2019).
| An Analysis of Energy Consumption and the Use of Renewables for a Small Drinking Water Treatment Plant.
| *Water*, 12(1), 1-21.


Cartridge Filtration Module
----------------------------------------

.. autoclass:: watertap3.wt_units.cartridge_filtration.UnitProcess
    :members: fixed_cap, elect, get_costing
    :exclude-members: build


..  raw:: pdf

    PageBreak