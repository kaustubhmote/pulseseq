"""
split_comb.py: combines datasets based on f1coeffs 
 
What it does
-----------
Take is a series of FIDs and splits them either sequentially or in 
an interleaved manner into 'N' different FIDS, (Eg A, B, C, D)
Takes in f1coeffs (Eg 1, -1, -1, 1) and combines the 'N' fids according to
the f1coeffs [A - B - C + D] 
 
Usage
-----
User is propmted for:
1. EXPNO to split and combine. This can be given in two ways,
2. Number of experiments to split up into
3. Sequentially splitting or interleaved splitting
2. F1COEFFs

Author
------
Kaustubh R. Mote 
 
Bugs and suggestions
--------------------
krmote @ tifrh.res.in
 
"""

import os
from sys import argv
import nmrglue as ng
import numpy as np
from base import dialog


# default imports from xcpy
name, curdir, curexpno, curprocno = argv
oexpno = curexpno + "00"


# get parameters from the user
iexpno, oexpno, split, arrangement, f1coeff, overwrite = dialog(
    header="Split Interleaved",
    info="Split an interleaved dataset",
    labels=[
        "Dataset to split and combine (EXPNO)",
        "EXPNO of combined dataset",
        "Number of experiments to split into",
        "How are multiple datasets arraged",
        "F1-COEFF (comma/whitespace separetd)",
        "Overwrite",
    ],
    types=["e", "e", "e", "d", "e", "c"],
    values=[curexpno, oexpno, "2", ["Interleaved", "Sequential"], "1 1", ""],
    comments=[],
)


# split and f1coeffs
split = int(split)
f1coeffs = [int(i) for i in f1coeff.replace(",", " ").split()]


# Check if an output directory exists if overwriting is not allowed
if "selected" not in overwrite:
    overwrite = False
    if os.path.isdir(os.path.join(curdir, oexpno)):
        raise ValueError("Expno {} exists!".format(oexpno))
else:
    overwrite = True


# check if number of f1coeffs and split matches
if len(f1coeffs) != split:
    raise ValueError(
        "Number of F1 coeffs do not match the number of experiments to split."
    )


# read the data
dic, data = ng.bruker.read(os.path.join(curdir, iexpno), read_pulseprogram=False, read_procs=True)


# get the dimension of data
ndim = dic["acqus"]["PARMODE"] + 1


# correct the number of increments and the number of scans
acqus_files = ["acqu{}s".format(i) for i in range(2, ndim + 1)]

# make a 2D data
inc = np.product(data.shape[:-1])
data = data.reshape(inc, -1)


# split data
outdata = {}
if arrangement == "Interleaved":
    for i in range(split):
        outdata[i] = data[i::split]
elif arrangement == "Sequential":
    td_one_exp = dic[acqus_files[-1]]["TD"] // split
    for i in range(split):
        outdata[i] = data[i * td_one_exp : (i + 1) * td_one_exp]


# combine data using f1coeffs
combined = np.zeros(outdata[i].shape, dtype=outdata[0].dtype)
for i in range(split):
    combined += f1coeffs[i] * outdata[i]


# correct the number of scans and increments in acqus files
dic[acqus_files[-1]]["TD"] = dic[acqus_files[-1]]["TD"] // split
dic["acqus"]["NS"] = dic["acqus"]["NS"] * split


# write
odir = os.path.join(curdir, oexpno)
ng.bruker.write(
    odir,
    dic,
    combined,
    write_prog=False,
    write_procs=True,
    pdata_folder=True,
    overwrite=overwrite,
)
