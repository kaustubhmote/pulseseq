"""
This file includes some utilities, mainly the paths that are used
to store temporary scripts and the specific python version that 
needs to be used in the script. The variables 'cpython', 'toppath',
and 'script' are imported in all the programs that are based on
this
"""
import sys, os

# CPYTHON installation to be used for processing

# Linux
# Change this line to point the python you want to use. 
# Eg '/usr/bin/python' or '/usr/bin/python3'. Use full filepaths
# Else, you can use python from a specific environment as is# given below. 
# This python should have access to nmrglue, numpy, scipy. 

# Mac
# Untested

# Windows:
# Use <pythonpath>\python.exe as your path. This python should have access
# to nmrglue, scipy and numpy
# All Popen processes in files should be run via shell in Windows
# For all scripts, add 'shell=True' argument to all 'Popen' functions

# TODO: make the subprocess commands OS agnostic
cpython = '/home/kaustubh/miniconda/envs/nmr-py37/bin/python'

# Folder of the TOPSPIN directory
try:
    # TOPSPIN > 3.1
    toppath = sys.registry['XWINNMRHOME'] 
except:
    # TOPSPIN < 3.1
    toppath = sys.getEnviron()['XWINNMRHOME'] 

# Temperory CPYTHON script that will created
scriptname = os.path.join(toppath, 'exp', 'stan', 'nmr', 'py', 'user', 'temp.py')

