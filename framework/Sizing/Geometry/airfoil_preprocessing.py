"""" 
Function  : airfoil_preprocessing.py
Title     : Airfoil pre-processing
Written by: Alejandro Rios
Date      : September/2019
Last edit : August/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This module takes as input the airfoil cordinates .dat file an redefine number of panels

Future implementations:
    - Redefine airfoil to create blunt trailing edge in order to prevent numerical errors

Inputs:
    - Aifoil name [str]
    - Panel number [int]
Outputs:
    - Airfoil.dat
"""
########################################################################################
"""Importing Modules"""
########################################################################################
########################################################################################
"""Function definition"""
########################################################################################




import os
import scipy as sp
from scipy.optimize import differential_evolution
from scipy import interpolate
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def airfoil_preprocessing(airfoil, panel_number):
    delimiter = '1'
    xfoil_run_file = 'xfoil_preproc.txt'
    panel_number = str(panel_number)
    ########################################################################################
    """Xfoil file writting"""
    ########################################################################################
    fid = open(xfoil_run_file, "w")
    fid.write("DELI" + delimiter + "\n")
    fid.write("load \n")
    fid.write("" + airfoil + ".dat" "\n\n")
    fid.write("PPAR\n")
    fid.write("N " + panel_number + "\n")
    fid.write("\n\n")
    fid.write("SAVE \n")
    fid.write("" + airfoil + ".dat" "\n")
    fid.write("Y \n")
    fid.write("QUID \n")
    fid.close()
    ########################################################################################
    """Xfoil Execution"""
    ########################################################################################
    # Xfoil run
    os.system("xfoil < xfoil_preproc.txt > NUL.dat")

    # Files cleaning
    if os.path.exists(xfoil_run_file):
        os.remove(xfoil_run_file)

    if os.path.exists(':00.bl'):
        os.remove(':00.bl')

    if os.path.exists('NUL.dat'):
        os.remove('NUL.dat')
    return
