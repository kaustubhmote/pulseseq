import sys, os
from subprocess import Popen, PIPE, STDOUT

# Scripts to run
python = '/home/kaustubh/miniconda/envs/nmr-py37/bin/python'
scriptdir = '/opt/topspin3.5pl7/exp/stan/nmr/py/user/'
script = os.path.join(scriptdir, 'temp.py')

# Get Input from user
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
import subprocess
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

dic, data = ng.bruker.read(indir)
data *= np.exp(1j * phase) 

subprocess.run(['cp', '-r', indir, outdir])
ng.bruker.write(outdir, dic, data, overwrite=True)
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

    with open(script, 'w') as outfile:
        outfile.write(cpyscript)

    p = Popen([python, script, curdir, iexpno, oexpno, phase], 
           stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    p.stdin.close()

    # Alert if the actual script fails 
    el = []	
    for line in iter(p.stdout.readline, ''):
        el.append(line)
	 
    if not el:
        MSG('Program ended successfully')
    else:
        MSG(''.join(el))

    p.stdout.close()
    p2 = Popen(['rm', 'temp.py'])

else:
    MSG('Aborted. Nothing written.')
