'''
This file includes some utilities, mainly the paths that are used
to store temporary scripts and the specific python version that 
needs to be used in the script.

Author
------
Kaustubh R. Mote

Bugs/Suggestions
----------------
kaustuberm@tifrh.res.in
'''

import sys, os
from subprocess import Popen, PIPE, STDOUT

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

cpython = '/home/kaustubh/miniconda/envs/nmr-py37/bin/python'

# Folder of the TOPSPIN directory
try:
    # TOPSPIN > 3.1
    toppath = sys.registry['XWINNMRHOME'] 
except:
    # TOPSPIN < 3.1
    toppath = sys.getEnviron()['XWINNMRHOME'] 

# Get current data folders
try:
    cd = CURDATA()
    curdir = os.path.join(cd[3], cd[0])
    curexpno = cd[1]
    curprocno = cd[2]
except:
    raise ValueError('No datafolder detected.
    You have to join an experient to execute this command.')

# get scriptname
cpyscript = sys.argv[1]
scriptname = os.path.join(toppath, 'exp', 'stan', 'nmr',
                          'py', 'user', 'cpython', cpyscript)

if os.path.isfile(scriptname):
    # TO DO: make the subprocess commands OS agnostic
    p = Popen([cpython, scriptname, curdir, curexpno, curprocno], 
               stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    p.stdin.close()

    # Alert if the actual script fails 
    errmsg = []	
    for line in iter(p.stdout.readline, ''):
       errmsg.append(line)
             
    if not errmsg:
        MSG('Program ended successfully')
    else:
        MSG(''.join(errmsg))
else:
    MSG('{} does not exist'.format(scriptname))
