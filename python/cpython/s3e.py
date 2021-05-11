"""
s3e.py: Applies the s3e filter 
 
What it does
-----------
Applies the S3E filter to a series of interleaved in-phase and anti-phase spectra

 
Usage
-----
User is propmted for:
1. EXPNO to split and combine. This can be given in two ways,
2. OUTPUT EXPNO

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
import matplotlib.pyplot as plt


# default imports from xcpy
name, curdir, curexpno, curprocno = argv
oexpno = curexpno + "00"


# get parameters from the user
iexpno, oexpno, zf, jcoupling, overwrite = dialog(
    header="Split Interleaved",
    info="Split an interleaved dataset",
    labels=[
        "Dataset to apply the S3E filter to",
        "EXPNO of OUTPUT dataset",
        "Zero filling for calculation",
        "J-Coupling",
        "Overwrite",
    ],
    types=["e", "e", "e", "e", "c"],
    values=[curexpno, oexpno, "32768", "52", ""],
    comments=[],
)


dic, data = ng.bruker.read(
    os.path.join(curdir, iexpno), read_pulseprogram=False, read_procs=True
)

td = data.shape[-1]

data = data.reshape(-1, td)
data = [data[0::2], data[1::2]]
data = [ng.proc_base.zf_size(d, size=int(zf)) for d in data]
data = [ng.proc_base.fft(d) for d in data]
data = [ng.bruker.remove_digital_filter(dic, d) for d in data]
data = [data[0] + data[1], data[0] - data[1]]
data = [ng.proc_autophase.autops(d, fn="acme", disp=False) for d in data]

udic = ng.bruker.guess_udic(dic, data[0])
uc = ng.fileiobase.uc_from_udic(udic)
xscale = uc.hz_scale()[:2]
delta = xscale[1] - xscale[0]
shift = int(float(jcoupling) / delta / 2)

data = [np.roll(data[0], shift), np.roll(data[1], -shift)]
data = data[0] + data[1]

if data.shape[0] == 1:
    data = ng.proc_autophase.autops(data, "acme", disp=False)
else:
    data = ng.proc_autophase.autops(data[0], "acme", disp=False)


grpdly = dic["acqus"]["GRPDLY"]
# fid = ng.proc_base.ps(data, p1=360 * grpdly)
fid = ng.proc_base.ifft_norm(data)
fid = [np.roll(f, int(grpdly)) for f in fid]
fid = np.array([f[: td] for f in fid])


print(fid.shape)

dic["acqus"]["NBL"] = 1
dic["acqu2s"]["TD"] = dic["acqu2s"]["TD"] // 2

ng.bruker.write(
    os.path.join(curdir, oexpno),
    dic,
    fid,
    bin_file="ser",
    write_procs=True,
    write_acqus=True,
    write_prog=False,
    pdata_folder=True,
)
