"""
term.py

Opens a terminal from topspin to the required dataset, expno or procno

"""

# Imports
import os
from sys import argv


# Get current data folders from inbuilt Jython fnctions
cd = CURDATA()
curdir = os.path.join(cd[3], cd[0])
curexpno = cd[1]
curprocno = cd[2]


# Parse argument to see where to go
if len(argv) == 1:
    argv.append("e")

if argv[1] == "d":
    dirc = curdir

elif argv[1] == "e":
    dirc = os.path.join(curdir, curexpno)
    
elif argv[1] == "p":
    dirc = os.path.join(curdir, curexpno, "pdata", curprocno)


# open a terminal to the required working directory
# choose one of the lines below depending on your terminal emulator
# or add a line

os.system("kitty -d {}".format(dirc))
# os.system("gnome-terminal --working-directory={}".format(dirc))
