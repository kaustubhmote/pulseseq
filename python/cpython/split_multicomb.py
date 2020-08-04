'''
split_multicomb.py: combines datasets based on given matrices 
 

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
3. There is an option to manually put in an arbitrary matrix. 
    Follwing is an example of an acceptable matrix:
    [1, 1, 1,   1]
    [1, 1, -1, -1]
    [1, -1, -1, 1]
    [1, -1, 1, -1]
   This will take consequitive FIDs and split them in the same
   manner as is shown in the "What it does" example above


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
from base import dialog, text_entry


def parse_matrix(rmat_string='', remove='#[];,'):
    rmat = []
    
    rmat_string = rmat_string.split('\n')
    rmat_string = [i for i in rmat_string if i != '']
    
    for i in rmat_string:
        for j in remove:
            i = i.replace(j, ' ')
        rmat.append(i) 

    rmat = np.array([np.fromstring(i, sep=' ', dtype='int32') for i in rmat])

    return rmat


# default imports from xcpy
name, curdir, curexpno, curprocno = argv
oexpno = curexpno + '00'

# get parameters from the user
iexpno, oexpno, rmat, overwrite = dialog(
            header='Split Multicomb',
            info='Split and combine an interleaved dataset in multiple ways',
            labels=['Dataset to split and combine (EXPNO)', 
                   '1st EXPNO of combined dataset', 
                   'Recombination Matrix',
                   'Overwrite'],
            types=['e', 'e', 'd', 'c'],
            values=[curexpno, oexpno, ['Manual', 'Pulseprogam Info', 'Hadamard'], ''],
            comments=[])


# Generate a Recombination Matrix

# Manual Entry for the Matrix
if rmat == 'Manual':
    rmat = text_entry()
    rmat = parse_matrix(rmat)
    rdim = rmat.shape[-1]
    numexp = rmat.shape[0]


# Standard Hadamard Matrix
elif rmat == 'Hadamard':
    
    # get dimension of hadamard matrix from the user
    rdim = dialog(header='Split Multicomb',
                  info='Enter the dimension of the Hadamard Matrix (N x N)',
                  labels=['Dimension'], 
                  types=['e'], 
                  values=['2'], 
                  comments=[''])

    rdim = int(rdim[0])
    # make a hadamard matrix of the appropriate dimension
    from scipy.linalg import hadamard
    rmat = hadamard(rdim)


# Pulseprogram info
elif rmat == 'Pulseprogram Info':
    rmat = []
    with open(os.path.join(curdir, curexpno, 'pulseprogram')) as infile:
        copy_flag = False
        for line in infile:
            if 'recombination_matrix_start' in line.strip():
                copy_flag = True
            if 'recombination_matrix_end' in line.strip():
                copy_flag = False
            elif copy_flag:
                rmat.append(line)

    rmat = parse_matrix(rmat)
    rdim = rmat.shape[-1]


# Check if an output directory exists if overwriting is not allowed
if 'selected' not in overwrite:
    overwrite = False
    for i in range(rdim):
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
td = dic['acqus']['TD']
inc = np.product(data.shape[:-1])
data = data.reshape(inc, -1)


# check that data dimensions make sense for the given recombination matrix
if data.shape[0] % rdim != 0:
    print(f'''Shape of recombination matrix ({rmat.shape}) incompatible with current data. 
    Data will be truncated to the nearest possible increment.''')
    nearest_allowed_inc = int(data.shape[0] // rdim * rdim)
    data = data[:nearest_allowed_inc]


# split data
outdata = np.empty((rdim, data.shape[0] // rdim * data.shape[-1]), dtype=data.dtype) 
for i in range(rdim):
    outdata[i] = data[i::rdim].reshape(-1)


# combine data using recombination matrix

recombined = rmat @ outdata
recombined = np.array([i.reshape(data.shape[0]//rdim, data.shape[-1]) for i in recombined])
 

# correct the number of scans and increments in acqus files
dic[acqus_files[-1]]['TD'] = data.shape[0] // rdim
dic['acqus']['NS'] =  dic['acqus']['NS'] * rdim


# write out multiple datasets
for i in range(numexp):
    odir = os.path.join(curdir, str(int(oexpno)+i)) 
    ng.bruker.write(odir, dic, recombined[i], write_prog=False, 
                    write_procs=True, pdata_folder=True,
                    overwrite=overwrite)
