.. _watertap3_overview:

WaterTAP3 Overview
========================

The Water Technoeconomic Assessment Pipe-Parity Platform (WaterTAP3) was developed under the
National Alliance for Water Innovation (NAWI) to facilitate consistent technoeconomic assessments
of desalination treatment trains. It is an analytically robust modeling tool that can be used to
evaluate cost, energy, and environmental tradeoffs of water treatment technology
across different water sources, sectors, and scales.

WaterTAP3 is publicly accessible and based on open-source models and data. The model is designed
to be flexible and customizable to allow users to adapt or create new treatment trains and process
models to assess different water treatment performance criteria.

Examples of WaterTAP3 applications include:

    * Baselining the state of water treatment systems across key water-using economic sectors.
    * Road-mapping critical technology development priorities to achieve pipe parity.
    * Performing ongoing project evaluation for NAWI funded research.
    * Conducting technoeconomic and life-cycle assessments of water technologies and systems
      across the water industry (in development).
|

.. _watertap3_installation:

WaterTAP3 Installation
----------------------------

WaterTAP3 is still in development so is not listed in ``pip`` and must be accessed by cloning the
current GitHub repo available at https://github.com/NREL/WaterTAP3:

#. Install the Anaconda distribution of Python:

    * https://www.anaconda.com/products/individual

#. Create new empty directory for WaterTAP3 installation:

    * e.g. this might be a folder called ``wt3`` on your desktop

#. Open terminal and navigate to that directory:

    * e.g. ``cd ~/Desktop/wt3``

#. Clone the repo:

    * In terminal, enter ``git clone https://github.com/NREL/WaterTAP3``
    * For example, if you cloned the repo into ``~/Desktop/wt3`` , you will have a new
      directory ``~/Desktop/wt3/WaterTAP3``
    * All the necessary python files and data files will be downloaded into the ``WaterTAP3``
      directory.

#. Navigate to ``~/WaterTAP3``. This directory contains the ``watertap3.yml`` file that is used
   to create the ``watertap3`` Python environment.

#. Create the ``watertap3`` Python environment:

    * In terminal, enter ``conda env create --file watertap3.yml``

#. Activate the ``watertap3`` Python environment:

    * In terminal, enter ``conda activate watertap3``

#. Navigate to ``~/WaterTAP3/watertap3``. This directory contains the ``setup.py`` file that is
   used to install ``watertap3`` as an editable Python package.

    * For example, if you cloned the repo into ``~/Desktop/wt3``, your working directory
      should now be ``~/Desktop/wt3/WaterTAP3/watertap3``.
    * This is also the directory that contains this documentation.

#. Install ``watertap3`` as an editable Python package:

    * Must be in directory containing ``setup.py`` file
    * In terminal, enter ``python –m pip install –e .``

        * **NOTE: MUST INCLUDE THE PERIOD AT THE END OF THIS COMMAND**

    * You should end up with new directory ``watertap3.egg-info`` in current directory

#. Start Jupyter Notebook app or Jupyter Lab app to access tutorial notebooks and run WaterTAP3:

    * For Jupyter Notebook - ``jupyter notebook``
    * For Jupyter Lab - ``jupyter lab``

|

.. _watertap3_cost_estimates:

WaterTAP3 Cost Estimates
----------------------------

Cost estimations are represented at the unit process level (i.e. per treatment technology in the
train) and aggregated to the system-level. Estimated costs include:

* Capital investment
* Annual operation and maintenance

    * Fixed (labor, maintenance)
    * Variable (energy, chemical)
|

.. _watertap3_outputs:

WaterTAP3 Outputs
----------------------------

The key performance metrics from WaterTAP3 currently include:

    * Levelized Cost of Water (LCOW): cost per unit of treated water
    * Energy intensity: direct energy consumption per unit of treated water
    * Water recovery: the percentage of water recovered for a beneficial use
    * Constituent removal: the percentage of constituent mass removed from the source water
|
Other outputs in development include:

    * Extent of alternative water and energy resources
    * Life-cycle assessment of environmental impacts (e.g. greenhouse gas emissions, total water
      intensity)
    * System resiliency and security

|

.. _watertap3_impacts:

WaterTAP3 Impacts
-----------------------------

The objective of WaterTAP3 is to become a standard tool to evaluate water treatment system
performance across key metrics used to promote and assess pipe-parity for a range of users
including industry and academia. The results from WaterTAP3 can help identify trade-offs among
the different performance metrics and enable users to asses how particular technologies affect
pipe-parity metrics and how improvements in one metric can affect others across a range of source
water conditions and technology performance parameters.

The flexibility and comprehensive scope of WaterTAP3 make it a useful tool for industry-wide
technoeconomic analyses, promoting better informed water investment decisions and technology
development. The tool can be used by policymakers, planners, and others without extensive
analytical experience through the publicly available graphical user interface (under development).



..  raw:: pdf

    PageBreak

