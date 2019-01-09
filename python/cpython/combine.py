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
from sys import argv
import nmrglue as ng
import numpy as np
from base import dialog

# default imports from xcpy
name, curdir, curexpno, curprocno = argv


# get the parameters from the user
oexpno = curexpno + '00'
iexpno, oexpno, numexpt, f1coeff, overwrite = dialog(
            header='Combine Experiments',
            info='Combine Mutiple experiments with f1coeffs',
            labels=['EXPNOs or Initial EXPNO to combine', 
                   'EXPNO for combined dataset', 
                   'Number of EXPNOs to combine',
                   'F1-COEFF (comma/whitespace separetd)',
                   'Overwrite'],
            types=['e', 'e', 'e', 'e', 'c'],
            values=[curexpno, oexpno, '2', '1 1', ''],
            comments=['', '', '(Optional)', '', ''])


# check if a single experiment number is given
iexpno = iexpno.replace(',', ' ').split()
iexpno = [int(i) for i in iexpno]


# Check if an output directory exists if overwriting is not allowed
if 'selected' not in overwrite:
    overwrite = False
    if os.path.isdir(os.path.join(curdir, oexpno)):
        raise ValueError('Expno {} exists!'.format(oexpno))
else:
    overwrite = True


if len(iexpno) == 1:
    numexpt = int(numexpt)
    iexpno = list(range(iexpno[0], iexpno[0]+numexpt))
else:
    numexpt = len(iexpno)


# check if there are atleast 2 experiments give to combine
if len(iexpno) < 2:
    raise ValueError('Need atleast two experiments to combine')


# get f1coeffs
f1coeffs = [int(i) for i in f1coeff.replace(',', ' ').split()]
if len(f1coeffs) != len(iexpno):
    raise ValueError('F1 coeffs do not match number of experiments to split')


# containers for datasets and datashapes
dataset, datashapes = {}, []
# read in experiments
for expno in iexpno:
    dic, data = ng.bruker.read(os.path.join(curdir, str(expno)), 
                read_pulseprogram=False)
    
    # get data dimensions
    ndim = dic['acqus']['PARMODE'] + 1
    if ndim > 1:
        inc = np.product(data.shape[:-1])
        data = data.reshape(inc, -1)
        datashapes.append(data.shape)

    # store in the container
    dataset[expno] = dic, data


# check if all datasets have the same shape
if len(set(datashapes)) > 1:
    raise ValueError('Not all datasets have the same size')


# initilise a matrix to fill in combined dataset
combined = np.zeros(dataset[iexpno[0]][1].shape, 
                    dtype=dataset[iexpno[0]][1].dtype)


# combine using the f1coeffs
for i, j in enumerate(iexpno):
    combined += f1coeffs[i] * dataset[j][1]


# correct for the NS
dic = dataset[iexpno[0]][0] 
dic['acqus']['NS'] = dic['acqus']['NS'] * numexpt 
if 'acqu' not in dic.keys():
    dic['acqu'] = dic['acqus']
dic['acqu']['NS'] = dic['acqu']['NS'] * numexpt


# set output directory
odir = os.path.join(curdir, oexpno)
# write
ng.bruker.write(odir, dic, combined, overwrite=overwrite, 
                write_procs=True, pdata_folder=True,
                write_prog=False, )
