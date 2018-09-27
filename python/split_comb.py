'''
split_il.py: Splits a ser file with 'n' ilterleaved datasets
            into individual datasets 
 
 What it does
 -----------
 If a ser file with 100 fids is arranged as follows:
 FID000, FID001, FID002, ... FID99, 
 using split=4 will first generate the following files:
 [A] FID000, FID004, FID008 ...
 [B] FID001, FID005, FID009 ...
 [C] FID002, FID006, FID010 ...
 [D] FID003, FID007, FID011 ...

 and these will then be combined using f1coeffs
 Eg, if f1coeffs = 1, -1, -1, 1;
 output file will be [A - B - C + D]
 
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
 
'''

import os
from subprocess import Popen, PIPE, STDOUT 
from base import cpython, toppath, scriptname

curdir = CURDATA()
idir = os.path.join(curdir[3], curdir[0])
iexpno, oexpno = curdir[1], curdir[1] + '00'

iexpno, oexpno, split, f1coeff = INPUT_DIALOG(
            title='Split Interleaved',
            header='Split an interleaved dataset',
            items=['Dataset to split and combine (EXPNO)', 
                   'EXPNO of combined dataset', 
                   'Number of experiments to split into',
                   'f1coeff (comma/whitespace separetd)'],
            values=[iexpno, oexpno, '2', '1 1'],
            types=['', '', '', ''])

cpyscript = '''
import os
from sys import argv
import nmrglue as ng
import numpy as np

idir, iexpno, oexpno, split, f1coeff = argv[1:]
split = int(split)
f1coeffs = [int(i) for i in f1coeff.replace(',', ' ').split()]

if len(f1coeffs) != split:
    print('F1 coeffs do not match number of experiments to split')
else:
    dic, data = ng.bruker.read(os.path.join(idir, iexpno))
    ndim = dic['acqus']['PARMODE'] + 1

    td = [1] * ndim
    for i in range(ndim):
        if i==0:
            td[i] = dic['acqus']['TD'] // 2
        else:
            td[i] = dic['acqu' + str(i+1) + 's']['TD']

    for acqfile in 'acqu2', 'acqu2s':
        dic[acqfile]['TD'] = td[1] // split

    inc = np.product(td[1:])
    data = data.reshape(inc, -1)

    outdata = {} 
    for i in range(split):
        outdata[i] = data[i::split]

    combined = np.zeros(outdata[i].shape, dtype=outdata[0].dtype)
    for i in range(split):
        combined += f1coeffs[i] * outdata[i]

    odir = os.path.join(idir, oexpno) 
    ng.bruker.write(odir, dic, combined, make_pdata=True, overwrite=True)
'''

with open(scriptname, 'w') as scriptfile:
    scriptfile.write(cpyscript)

p = Popen([cpython, scriptname, idir, iexpno, oexpno, split, f1coeff], 
           stdin=PIPE, stdout=PIPE, stderr=STDOUT)
p.stdin.close()

errmsg = ''
for line in iter(p.stdout.readline, ''):
    errmsg += line

if errmsg:
    MSG(errmsg)
else:
    MSG('Finished Succesfully')
