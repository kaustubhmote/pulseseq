"""
This file includes some utilities, mainly the paths that are used
to store temporary scripts and the specific python version that 
needs to be used in the script. The variables 'cpython', 'toppath',
and 'script' are imported in all the programs that are based on
this
"""
import sys, os

# Change this line to point the python you want to use. If you want to
# python installation from your system, just change it to 'python', 'python2',
# or 'python3'. Else, you can use python from a specific environment as is
# given below. If you plan to use NMRGlue, make sure that this python has 
# access to numpy and scipy libraries
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

