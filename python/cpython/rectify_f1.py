'''
rectify_f1.py: correct the f1 dimension spectral width and frequency


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
iexpno, oexpno, f1_nuc, overwrite = dialog(
                  header='Rectify F1 dimension parameters',
                  info='Correct the parameters for the F1 dimension',
                  labels=['EXPNO of the dataset to correct',
                          'EXPNO of the output dataset',
                          'Correct F1 nucleus (Channel number from \'EDASP\')',
                          'Overwrite'],
                  types=['e', 'e', 'd', 'c'],
                  values=[curexpno, oexpno, list(range(1, 7)), ''],
                  comments=['', '', '', ''])


# see if overwriting is allowed
if 'selected' in overwrite:
    overwrite = True
else:
    overwrite = False


indir = os.path.join(curdir, iexpno)
outdir = os.path.join(curdir, oexpno)


# read the data
dic, data = ng.bruker.read(indir, read_acqus=True)


# change the processing frequency for F1 dimension
dic['acqu2s']['NUC1'] = dic['acqus'][f'NUC{f1_nuc}']
dic['acqu2s']['SW'] *= dic['acqu2s']['BF1'] / dic['acqus'][f'BF{f1_nuc}']
dic['acqu2s']['BF1'] = dic['acqus'][f'BF{f1_nuc}']
dic['acqu2s']['O1'] = dic['acqus'][f'O{f1_nuc}']
dic['acqu2s']['SFO1'] = dic['acqus'][f'SFO{f1_nuc}']
dic['proc2s']['SF'] = dic['acqus'][f'SFO{f1_nuc}']


# write out the file
ng.bruker.write(outdir, dic, data, write_prog=False, write_acqus=True, 
                write_procs=True, pdata_folder=True, overwrite=overwrite)
