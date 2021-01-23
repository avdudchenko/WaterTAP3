from pylab import *

import shutil
import sys
import os.path
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.optimize import minimize
import itertools
import pyomo.environ as env
import ast
from pyomo.environ import *
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

### WATER TAP MODULES ###
import importfile
import module_import
import design

from pyomo.environ import ConcreteModel, SolverFactory, TransformationFactory
from pyomo.network import Arc, SequentialDecomposition
import pyomo.environ as env

from idaes.core import FlowsheetBlock

# Import properties and units from "WaterTAP Library"
from water_props import WaterParameterBlock
#from model_example import UnitProcess
from source_example import Source
from split_test2 import Separator1

from mixer_example import Mixer1

import financials
import display
import watertap as wt
import case_study_trains

from pyomo.environ import ConcreteModel, SolverFactory, TerminationCondition, \
    value, Var, Constraint, Expression, Objective, TransformationFactory, units as pyunits
from pyomo.network import Arc, SequentialDecomposition
from idaes.core import FlowsheetBlock
from idaes.generic_models.unit_models import Mixer, Pump

from idaes.generic_models.unit_models import Separator as Splitter

from idaes.core.util.model_statistics import degrees_of_freedom
from pyomo.util.check_units import assert_units_consistent
import pyomo.util.infeasible as infeas
import idaes.core.util.scaling as iscale
#from src import treatment_train_design
#from src import display
#from src import get_graph_chars
#from src import filter_processes
#from src import post_processing
#from src import get_model_chars
#from src import save_train_module
#from src import module_import
#from src import model_constraints #as mc
#from src import load_train_module

### units that pre-exist ###
unit_process_library_list = [
    "chlorination_twb",
    "media_filtration_twb",
    "microfiltration_twb",
    "ultrafiltration_twb",
    "nanofiltration_twb",
    "coag_and_floc"
    "ro_twb",
    "uv_twb",
    "ro_bor",
    "uvozone_twb",
    "mbr",
    "water_pumping_station",
    "ro_deep",
    "media_filtration",
    "coag_and_floc",
    "lime_softening",
    "ro_deep",
    "treated_storage_24_hr",
    "sedimentation",
    "water_pumping_station",
    "sulfuric_acid_addition",
    "sodium_bisulfite_addition",
    "co2_addition",
    "ammonia_addition",
    "municipal_drinking",
    "sw_onshore_intake",
    "holding_tank",
    "tri_media_filtration",
    "cartridge_filtration"
]


fw_filename = "data/case_study_water_sources_and_uses.csv"
water_source_use_library = importfile.feedwater(
    input_file=fw_filename,
    reference=None,
    case_study=None,
    water_type=None,
    source_or_use=None,
)



def watertap_setup(dynamic = False):
    # Create a Pyomo model
    m = ConcreteModel()

    # Add an IDAES FlowsheetBlock and set it to steady-state
    m.fs = FlowsheetBlock(default={"dynamic": dynamic})

    # Add water property package (this can be updated to account for a more extensive list of properties)
    m.fs.water = WaterParameterBlock()

    return m


def run_water_tap(m):

    # Set up a solver in Pyomo and solve
    solver1 = SolverFactory('ipopt')
    results = solver1.solve(m, tee=True)

    # Transform Arc to construct linking equations
    TransformationFactory("network.expand_arcs").apply_to(m)
    seq = SequentialDecomposition()
    G = seq.create_graph(m)
    print("degrees_of_freedom:", degrees_of_freedom(m))

    # Display the inlets and outlets of each unit
    for node in G.nodes():
        print("----------------------------------------------------------------------")
        print(node)

        if "split" in (str(node).replace('fs.', '')): 
            getattr(m.fs, str(node).replace('fs.', '')).inlet.display()
            getattr(m.fs, str(node).replace('fs.', '')).outlet1.display()
            getattr(m.fs, str(node).replace('fs.', '')).outlet2.display()
        elif "use" in (str(node).replace('fs.', '')): 
            getattr(m.fs, str(node).replace('fs.', '')).inlet.display()
            getattr(m.fs, str(node).replace('fs.', '')).outlet.display()
        elif "mixer" in (str(node).replace('fs.', '')): 
            getattr(m.fs, str(node).replace('fs.', '')).inlet1.display()
            getattr(m.fs, str(node).replace('fs.', '')).inlet2.display()
            getattr(m.fs, str(node).replace('fs.', '')).outlet.display()
        else:
            getattr(m.fs, str(node).replace('fs.', '')).inlet.display()
            getattr(m.fs, str(node).replace('fs.', '')).outlet.display()
            getattr(m.fs, str(node).replace('fs.', '')).waste.display()


        print("Show some costing values")
        print("---------------------")

        if "source" in (str(node).replace('fs.', '')): 
            print("should skip:", (str(node).replace('fs.', '')))
            continue
        elif "use" in (str(node).replace('fs.', '')): 
            print("should skip:", (str(node).replace('fs.', '')))
            continue
        elif "split" in (str(node).replace('fs.', '')): 
            print("should skip:", (str(node).replace('fs.', '')))
            continue  
        elif "mixer" in (str(node).replace('fs.', '')): 
            print("should skip:", (str(node).replace('fs.', '')))
            continue
        else:
            print("should have a cost", (str(node).replace('fs.', '')))
            if getattr(m.fs, str(node).replace('fs.', '')).costing.total_up_cost() is not None:
                print("total_up_cost:" , 
                      getattr(m.fs, str(node).replace('fs.', '')).costing.total_up_cost())

            else:
                getattr(m.fs, str(node).replace('fs.', '')).costing.total_up_cost.display()

        print("----------------------------------------------------------------------")

def main():
    print("importing something")
    # need to define anything here?


if __name__ == "__main__":
    main()