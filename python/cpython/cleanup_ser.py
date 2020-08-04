"""
cleanup_ser.py
If a 3D experiment is stopped midway, only a part of the plane that was
incomplete is stored. This causes issues in further processing. As far
as I can tell, Topspin ignores the incomplete plane altogether in the 
data processing. This script reads in the file and writes back out only 
planes that are complete

Usage
-----
User will be prompted for the experiment number to output the cleaned up 
file to. This is the EXPNO in the current folder 

Author
------
Kaustubh R. Mote

Bugs/Suggestions
----------------
krmote@tifrh.res.in

"""
import os
import nmrglue as ng
import numpy as np
from sys import argv
from base import dialog

name, curdir, curexpno, curprocno = argv

# Get output directory from user
oexpno = curexpno + "00"
oexpno, overwrite = dialog(
    header="Cleanup SER File",
    info="Removes planes from a 3D that are not completely acquired",
    labels=["Output EXPNO", "Ovewrite"],
    types=["e", "c"],
    values=[oexpno, ""],
    comments=["", ""],
)
indir = os.path.join(curdir, curexpno)
outdir = os.path.join(curdir, oexpno)

# Check if an output directory exists if overwriting is not allowed
if "selected" not in overwrite:
    if os.path.isdir(os.path.join(curdir, str(int(oexpno)))):
        raise ValueError("Expno {} exists!".format(str(int(oexpno) + i)))

# Read the data
dic, data = ng.bruker.read(indir)

# Number of dimensions
ndim = dic["acqus"]["PARMODE"] + 1
if ndim != 3:
    raise ValueError("Program suitable only for 3D dataset")

# Get TD values from acqus files
td = [dic[f]["TD"] for f in ["acqu3s", "acqu2s", "acqus"]]

# Make the data a 1D array
data = data.reshape(-1)

# Find total number of points that should be present, incl zeros
td[2] = int(np.ceil(td[2] / 256.0) * 256) // 2
npoints = np.product(td)

# reshape so that there is one FID per row
data = data[0:npoints].reshape(td[0] * td[1], -1)

# write out the SER file, make pdata folders
ng.bruker.write(outdir, dic, data, write_procs=True, pdata_folder=True, overwrite=True)
