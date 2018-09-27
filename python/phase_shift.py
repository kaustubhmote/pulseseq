'''
phase_shift: adds an arbitrary phase shift to the raw FID/SER file
and writes it to a new directory

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

outdir, phase = INPUT_DIALOG(title='Shift the phase of raw FID',
                header='',
                items=['Destinantion EXPNO', 'Phase Shift (Degrees)'],
                values=[oexpno, '0'], 
                types=['', ''], 
                comments=['1', '1'])

cpyscript = '''
import os
import nmrglue as ng
import numpy as np
from sys import argv

curdir = argv[1]
curexpno = argv[2] 
outexpno = argv[3]
phase = np.pi/180 * float(argv[4])

indir = os.path.join(curdir, curexpno)
outdir = os.path.join(curdir, outexpno)

dic, data = ng.bruker.read(indir, read_procs=True)
data *= np.exp(1j * phase) 

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

    p = Popen([cpython, scriptname, curdir, iexpno, oexpno, phase], 
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
    p2 = Popen(['rm', 'temp.py'])

else:
    MSG('Aborted. Nothing written.')
