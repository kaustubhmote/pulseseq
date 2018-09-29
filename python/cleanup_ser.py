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

import sys, os
from subprocess import Popen, PIPE, STDOUT
from base import cpython, toppath, scriptname

cd = CURDATA()
curdir = os.path.join(cd[3], cd[0])
iexpno = cd[1]
oexpno = cd[1] + '00'

oexpno = INPUT_DIALOG(
             title='Remove incomplete plane in 3D',
             header='',
             items=['Destinantion EXPNO',],
             values=[oexpno,], 
             types=['',],)[0] 


cpyscript = '''
import os
import nmrglue as ng
import numpy as np
from sys import argv

curdir = argv[1]
curexpno = argv[2]
outexpno = argv[3]

indir = os.path.join(curdir, curexpno)
outdir = os.path.join(curdir, outexpno)
print(outdir)
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
'''

if os.path.exists(os.path.join(curdir, oexpno)):
    confirm = INPUT_DIALOG(title='Confirmation', 
        header='Destinantion Directory Exits! Type YES to overwrite',
        items=['Overwrite EXPNO ' + oexpno +'?'],
        values=['No'],
        types=[''])
else:

    confirm = ['yes']

if confirm[0].lower() in ['yes', 'y']:

    with open(scriptname, 'w') as outfile:
        outfile.write(cpyscript)

    p = Popen([cpython, scriptname, curdir, iexpno, oexpno], 
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

    p.stdout.close()
    p2 = Popen(['rm', scriptname])

else:
    MSG('Aborted. Nothing written.')
