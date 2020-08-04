"""
split_seq.py: Splits a ser file into 'n' sequentially
              acquired datasets
 
 What it does
 -----------
 If a ser file with 100 fids is arranged as follows:
 FID000, FID001, FID002, ... FID99, 
 using n=4 will make the following four ser files:
 1. FID00, FID01, FID02 ... FID24
 2. FID25, FID26, FID27 ... FID49
 3. FID50, FID51, FID52 ... FID74
 4. FID75, FID76, FID77 ... FID99

 Usage
 -----
 User is prompted for input of number of interleaved experiments
 and the first expno where the new ser files should be stored.
 Remaining ser files will be store in next N-1 consecutive 
 expnos  

 Author
 ------
 Kaustubh R. Mote 
 
 Bugs and suggestions
 --------------------
 kaustuberm @ tifrh.res.in
 
"""

import os
import nmrglue as ng
import numpy as np
from sys import argv
from base import dialog

name, curdir, curexpno, curprocno = argv

# Get output directory from user
oexpno = curexpno + "00"
iexpno, oexpno, split, overwrite = dialog(
    header="Split Sequential",
    info="Split a sequentially acquired dataset",
    labels=[
        "Dataset to split (EXPNO)",
        "EXPNO of 1st split dataset",
        "Number of experiments to split into",
        "Overwrite",
    ],
    types=["e", "e", "e", "c"],
    values=[curexpno, oexpno, 2, ""],
    comments=["", "", "", ""],
)

# Decipher variables
indir = os.path.join(curdir, iexpno)
split = int(split)


# Check if an output directory exists if overwriting is not allowed
if "selected" not in overwrite:
    overwrite = False
    for i in range(split):
        if os.path.isdir(os.path.join(curdir, str(int(oexpno) + i))):
            raise ValueError("Expno {} exists!".format(str(int(oexpno) + i)))
else:
    overwrite = True


# Read the data
dic, data = ng.bruker.read(indir)

# dimensionality of the experiment
ndim = dic["acqus"]["PARMODE"] + 1

# get number of indirect increments and reshape to have 1 FID per row
acqus_files = ["acqu{}s".format(i) for i in range(2, ndim + 1)]
inc = np.product([dic[f]["TD"] for f in acqus_files])
data = data.reshape(inc, -1)

# reset the number of increments in the last td
td_one_exp = dic[acqus_files[-1]]["TD"] // split
dic[acqus_files[-1]]["TD"] = td_one_exp


outdata = {}
for i in range(split):
    outdata[i] = data[i * td_one_exp : (i + 1) * td_one_exp]

for i in range(split):
    odir = os.path.join(curdir, str(int(oexpno) + i))
    ng.bruker.write(
        odir, dic, outdata[i], overwrite=overwrite, write_procs=True, pdata_folder=True
    )
