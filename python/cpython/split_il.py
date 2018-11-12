'''
split_il.py: Splits a ser file with 'n' ilterleaved datasets
            into individual datasets 
 
 What it does
 -----------
 If a ser file with 100 fids is arranged as follows:
 FID00, FID01, FID02, ... FID99
 using split=4 will make the following four ser files:
 1. FID00, FID04, FID08 ...
 2. FID01, FID05, FID09 ...
 3. FID02, FID06, FID10 ...
 4. FID03, FID07, FID11 ...
 
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
import nmrglue as ng
import numpy as np
from sys import argv
from base import dialog

name, curdir, curexpno, curprocno = argv

# Get output directory from user
oexpno = curexpno + '00'
iexpno, oexpno, split, overwrite = dialog(
                  header='Split Interleaved',
                  info='Split an interleaved dataset',
                  labels=['Dataset to split (EXPNO)',
                          'EXPNO of 1st split dataset',
                          'Number of experiments to split into',
                          'Overwrite'],
                  types=['e', 'e', 'e', 'c'],
                  values=[curexpno, oexpno, 2, ''],
                  comments=['', '', '', ''])

# Decipher variables
indir = os.path.join(curdir, iexpno)
outdir = os.path.join(curdir, oexpno)
split = int(split)

# Check if an output directory exists if overwriting is not allowed
if 'selected' not in overwrite:
    for i in range(split):
        if os.path.isdir(os.path.join(curdir, str(int(oexpno)+i))):
            raise ValueError('Expno {} exists!'.format(str(int(oexpno)+i)))

# Read the data
dic, data = ng.bruker.read(indir)

# Determine the dimensionality and the acqus files
ndim = dic['acqus']['PARMODE'] + 1
acqus_files = ['acqu{}s'.format(i) for i in range(2, ndim+1)]

# Calculate the number of indirect increments 
# and reshape to have 1 FID per row
inc = np.product([dic[f]['TD'] for f in acqus_files])
data = data.reshape(inc, -1)

# Correct the TD for the F1 dimenson 
td_one_exp = dic[acqus_files[-1]]['TD'] // split
dic[acqus_files[-1]]['TD'] = td_one_exp 


# Split the data
outdata = {} 
for i in range(split):
    outdata[i] = data[i::split]

# Write in 'split' number of dataset
for i in range(split):
    odir = os.path.join(curdir, str(int(oexpno) + i)) 
    ng.bruker.write(odir, dic, outdata[i], overwrite=True,
                    write_procs=True, pdata_folder=True)

