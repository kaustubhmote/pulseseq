import os
from subprocess import Popen, PIPE, STDOUT 
from base import cpython, toppath, scriptname

curdir = CURDATA()
idir = os.path.join(curdir[3], curdir[0])
iexpno, oexpno = curdir[1], curdir[1] + '00'

iexpno, oexpno, split = INPUT_DIALOG(
            title='Split Interleaved',
            header='Split an interleaved dataset',
            items=['Dataset to split (EXPNO)', 
                   'EXPNO of 1st split dataset', 
                   'Number of experiments to split into'],
            values=[iexpno, oexpno, '2'],
            types=['', '', ''])

cpyscript = '''
import os, subprocess
from sys import argv
import nmrglue as ng
import numpy as np

idir, iexpno, oexpno, split = argv[1:]
split = int(split)

dic, data = ng.bruker.read(os.path.join(idir, iexpno))
ndim = dic['acqus']['PARMODE'] + 1

td = [1] * ndim
for i in range(ndim):
    if i==0:
        td[i] = dic['acqus']['TD'] // 2
        dic['acqu'] = dic['acqus']
    else:
        td[i] = dic['acqu' + str(i+1) + 's']['TD']
        dic['acqu' + str(i+1)] = dic['acqu' + str(i+1) + 's']
inc = np.product(td[1:])
data = data.reshape(inc, -1)

outdata = {} 
for i in range(split):
    outdata[i] = data[i::split]

dic['acqu2s']['TD'] = td[1] // split

for i in range(split):
    odir = os.path.join(idir, str(int(oexpno) + i)) 
    idir_pdata = os.path.join(idir, iexpno, 'pdata') 
    ng.bruker.write(odir, dic, outdata[i], overwrite=True)
    subprocess.run(['cp', '-r', idir_pdata, odir])
'''

with open(scriptname, 'w') as scriptfile:
    scriptfile.write(cpyscript)

p = Popen([cpython, scriptname, idir, iexpno, oexpno, split], 
           stdin=PIPE, stdout=PIPE, stderr=STDOUT)
p.stdin.close()

errmsg = ''
for line in iter(p.stdout.readline, ''):
    errmsg += line

if errmsg:
    MSG(errmsg)
else:
    MSG('Finished Succesfully')
