'''
combine.py: combines datasets based on f1coeffs 
 
What it does
-----------
Takes in fids from multiple datasets (Eg A, B, C, D) 
Takes in f1coeffs (Eg 1, -1, -1, 1)
output file will be [A - B - C + D]
 
Usage
-----
User is propmted for:
1. EXPNO or EXPNOs to combine. This can be given in two ways,
   (i) EXPNO of a the first in a series to combine or (Eg. 100)
   (ii) List of EXPNOs to combine (Eg: 100, 101, 107)
    When a single EXPNO is give, the next N experiments given the
    value of 'Number of experiments to combine' is taken.
    If EXPNOs > 2, Number of experiments to combine are ignored
2. F1COEFFs

Author
------
Kaustubh R. Mote 
 
Bugs and suggestions
--------------------
kaustuberm @ tifrh.res.in
 
'''

import os
from subprocess import Popen, PIPE, STDOUT 
from base import cpython, toppath, scriptname

curdir = CURDATA()
idir = os.path.join(curdir[3], curdir[0])
iexpno, oexpno = curdir[1], curdir[1] + '00'

iexpno, oexpno, numexpt, f1coeff = INPUT_DIALOG(
            title='Combine Experiments',
            header='Combine Mutiple experiments with f1coeffs',
            items=['EXPNOs or Initial EXPNO to combine', 
                   'EXPNO for combined dataset', 
                   'Number of EXPNOs to combine',
                   'F1-COEFF (comma/whitespace separetd)'],
            values=[iexpno, oexpno, '0', '1 1'],
            types=['', '', '', ''],
            comments=['', '', '(Optional)', ''])
         

cpyscript = '''
import os
from sys import argv
import nmrglue as ng
import numpy as np

idir, iexpno, oexpno, numexpt, f1coeff = argv[1:]
iexpno = [int(i) for i in iexpno.replace(',', ' ').split()]
print(iexpno)

if len(iexpno) == 1:
    numexpt = int(numexpt)
    iexpno = list(range(iexpno[0], iexpno[0]+numexpt))
else:
    numexpt = len(iexpno)

if len(iexpno) < 2:
    raise ValueError('Need atleast two experiments to combine')

f1coeffs = [int(i) for i in f1coeff.replace(',', ' ').split()]
if len(f1coeffs) != len(iexpno):
    raise ValueError('F1 coeffs do not match number of experiments to split')

dataset, datashapes = {}, []


for expno in iexpno:
    dic, data = ng.bruker.read(os.path.join(idir, str(expno)), 
                read_pulseprogram=False)
    
    ndim = dic['acqus']['PARMODE'] + 1
    if ndim > 1:
        inc = np.product(data.shape[:-1])
        data = data.reshape(inc, -1)
        datashapes.append(data.shape)

    dataset[expno] = dic, data

if len(set(datashapes)) > 1:
    raise ValueError('Not all datasets have the same size')

combined = np.zeros(dataset[iexpno[0]][1].shape, 
                    dtype=dataset[iexpno[0]][1].dtype) 
for i, j in enumerate(iexpno):
    combined += f1coeffs[i] * dataset[j][1]

odir = os.path.join(idir, oexpno)

dic = dataset[iexpno[0]][0] 
dic['acqus']['NS'] = dic['acqus']['NS'] * numexpt 
dic['acqu']['NS'] = dic['acqu']['NS'] * numexpt

ng.bruker.write(odir, dic, combined, make_pdata=True,
                write_prog=False, overwrite=True)
'''

with open(scriptname, 'w') as scriptfile:
    scriptfile.write(cpyscript)

p = Popen([cpython, scriptname, idir, iexpno, oexpno, numexpt, f1coeff], 
           stdin=PIPE, stdout=PIPE, stderr=STDOUT)
p.stdin.close()

errmsg = ''
for line in iter(p.stdout.readline, ''):
    errmsg += line

if errmsg:
    MSG(errmsg)
else:
    MSG('Finished Succesfully')
