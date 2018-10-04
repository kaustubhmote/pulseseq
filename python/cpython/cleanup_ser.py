'''
cleanup_ser.py
If a 3D experiment is stopped midway, pnly a part of the plane that was
incomplete is stored. This causes issues in further processing. As far
as I can tell, Topspin ignores the incomplete plane altogether in the 
data processing. This script reads in the file and writes back out only 
planes that are complete

Usage
-----
User will be prompted for the experiment number to output the file to 
and the phase shift in degrees

Author
------
Kaustubh R. Mote

Bugs/Suggestions
----------------
kaustuberm@tifrh.res.in

'''
import os
import nmrglue as ng
import numpy as np
from sys import argv

name, curdir, curexpno, curprocno = argv

indir = os.path.join(curdir, curexpno)
outdir = os.path.join(curdir, outexpno)
dic, data = ng.bruker.read(indir,) 

ndim = dic['acqus']['PARMODE'] + 1
if ndim != 3:
    raise ValueError('Program suitable only for 3D dataset')

td = []
for f in ['acqu3s', 'acqu2s', 'acqus']:
    td.append(dic[f]['TD'])

td[2] = int(np.ceil(td[2]/256.) * 256) // 2
npoints = np.product(td)
print(npoints)
data = data.reshape(-1)
data = data[0:npoints].reshape(td[0]*td[1], -1)
ng.bruker.write(outdir, dic, data, make_pdata=True, overwrite=True)

