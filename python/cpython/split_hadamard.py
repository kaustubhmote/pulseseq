'''
split_hadamard.py: combines datasets based on hadamard matrices 
 
What it does
-----------
Take is a series of FIDs and splits them  in an interleaved manner into 'N' 
where N is the dimension of the hadamard matrix used to recombine
For example, with a hadamard dimension of 4 and 4 FIDS: A, B, C, D, the data 
will be first split into A, B, C, D and recombined as:
    (a) A+B+C+D
    (b) A+B-C-D
    (c) A-B-C+D
    (d) A-B+C-D
All for experiments will be returned in conseceutive experiments startig with
the output experiments number that is given
 
Usage
-----
User is propmted for:
1. EXPNO to split and combine. ,
2. Dimension of the hadamard matrix

Author
------
Kaustubh R. Mote 
 
Bugs and suggestions
--------------------
kaustuberm @ tifrh.res.in
 
'''

import os
from sys import argv
import nmrglue as ng
import numpy as np
from base import dialog
from scipy.linalg import hadamard


# default imports from xcpy
name, curdir, curexpno, curprocno = argv
oexpno = curexpno + '00'


# get parameters from the user
iexpno, oexpno, hdim, overwrite = dialog(
            header='Split Interleaved',
            info='Split an interleaved dataset',
            labels=['Dataset to split and combine (EXPNO)', 
                   'EXPNO of combined dataset', 
                   'Dimension of the Hadamard matrix',
                   'Overwrite'],
            types=['e', 'e', 'd', 'c'],
            values=[curexpno, '1000', [4, 2, 8, 16, 32, 64, 128], '',],
            comments=[])


# Check if an output directory exists if overwriting is not allowed
if 'selected' not in overwrite:
    overwrite = False
    for i in range(int(hdim)):
        if os.path.isdir(os.path.join(curdir, str(int(oexpno)+i))):
            raise ValueError('Expno {} exists!'.format(oexpno))
else:
    overwrite = True


# read the data
dic, data = ng.bruker.read(os.path.join(curdir, iexpno), 
                           read_pulseprogram=False)


# get the dimension of data
ndim = dic['acqus']['PARMODE'] + 1


# make a list of possible acquNs files
acqus_files = ['acqu{}s'.format(i) for i in range(2, ndim+1)]


# make a 2D data
inc = np.product(data.shape[:-1])
data = data.reshape(inc, -1)


# get the dimension of the hadamard matrix and make the hadamard matrix
hdim = int(hdim)
hmat = hadamard(hdim)


# check that data dimensions make sense for the given hadmard matrix
if data.shape[0] % hdim != 0:
    raise ValueError(f'Dimension of Hadamard matrix ({hdim}) incompatible with data')


# split data
outdata = np.empty((hdim, data.shape[0] // hdim * data.shape[-1]), dtype=data.dtype) 
for i in range(hdim):
    outdata[i] = data[i::hdim].reshape(-1)


# combine data using hadamard matrix
recombined = hmat @ outdata
recombined = np.array([i.reshape(data.shape[0]//hdim, data.shape[-1]) for i in recombined])
 
print(recombined[0].shape)

# correct the number of scans and increments in acqus files
dic[acqus_files[-1]]['TD'] = data.shape[0] // hdim
dic['acqus']['NS'] =  dic['acqus']['NS'] * hdim


# write out multiple datasets
for i in range(hdim):
    odir = os.path.join(curdir, str(int(oexpno)+i)) 
    ng.bruker.write(odir, dic, recombined[i], write_prog=False, 
                    write_procs=True, pdata_folder=True,
                    overwrite=overwrite)
