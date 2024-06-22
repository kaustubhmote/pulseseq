"""
rectify_f1.py: correct the f1 dimension spectral width and frequency


 Author
 ------
 Kaustubh R. Mote 
 
 Bugs and suggestions
 --------------------
 krmote @ tifrh.res.in
"""

import os
import nmrglue as ng
import numpy as np
from sys import argv
from base import dialog

name, curdir, curexpno, curprocno = argv

Flist = ["None"] + [f"F{i}" for i in range(1, 7)]


# Get output directory from user
oexpno = curexpno + "00"
iexpno, oexpno, nuc1, corr_nuc1, nuc2, corr_nuc2, overwrite = dialog(
    header="Rectify F1/2 dimension parameters",
    info="Correct the parameters for the F1 or F2 dimension",
    labels=[
        "EXPNO of the dataset to correct",
        "EXPNO of the output dataset",
        "Nucleus to correct (Dimension from ACQUPARS tab) I",
        "Correct nucleus (Channel number from 'EDASP') I",
        "Nucleus to correct (Dimension from ACQUPARS tab) II",
        "Correct nucleus (Channel number from 'EDASP') II",
        "Overwrite",
    ],
    types=["e", "e", "d", "d", "d", "d", "c"],
    values=[curexpno, oexpno, Flist, Flist, Flist, Flist, ""],
    comments=["", "", "", "", "", "", ""],
)

corr_nuc_list = []
afiles = []
pfiles = []

# Sanitize
if nuc1 != "None":
    nuc1 = int(nuc1[1])
    corr_nuc1 = int(corr_nuc1[1])
    corr_nuc_list.append(corr_nuc1)
    afiles.append(f"acqu{nuc1+1}s")
    pfiles.append(f"proc{nuc1+1}s")


if nuc2 != "None":
    nuc2 = int(nuc2[1])
    corr_nuc2 = int(corr_nuc2[1])
    corr_nuc_list.append(corr_nuc2)
    afiles.append(f"acqu{nuc2+1}s")
    pfiles.append(f"proc{nuc2+1}s")


# see if overwriting is allowed
if "selected" in overwrite or overwrite:
    overwrite = True
else:
    overwrite = False


if len(corr_nuc_list) == 0:
    print("Nothing to do. Exiting ...")

else:

    indir = os.path.join(curdir, iexpno)
    outdir = os.path.join(curdir, oexpno)

    # read the data
    dic, data = ng.bruker.read(indir, read_acqus=True, read_pulseprogram=False)

    for corr_nuc, acquns_file, procns_file in zip(corr_nuc_list, afiles, pfiles):
        # change the processing frequency for appropriate dimension
        dic[acquns_file]["NUC1"] = dic["acqus"][f"NUC{corr_nuc}"]
        dic[acquns_file]["SW"] *= (
            dic[acquns_file]["BF1"] / dic["acqus"][f"BF{corr_nuc}"]
        )
        dic[acquns_file]["BF1"] = dic["acqus"][f"BF{corr_nuc}"]
        dic[acquns_file]["O1"] = dic["acqus"][f"O{corr_nuc}"]
        dic[acquns_file]["SFO1"] = dic["acqus"][f"SFO{corr_nuc}"]
        dic[procns_file]["SF"] = dic["acqus"][f"SFO{corr_nuc}"]

    # write out the file
    ng.bruker.write(
        outdir,
        dic,
        data,
        write_prog=False,
        write_acqus=True,
        write_procs=True,
        pdata_folder=True,
        overwrite=overwrite,
    )
