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

Flist = [f"F{i}" for i in range(1, 7)]


# Get output directory from user
oexpno = curexpno + '00' 
iexpno, oexpno, nuc, corr_nuc, overwrite = dialog(
                  header='Rectify F1/2 dimension parameters',
                  info='Correct the parameters for the F1 or F2 dimension',
                  labels=['EXPNO of the dataset to correct',
                          'EXPNO of the output dataset',
                          'Nucleus to correct',
                          'Correct nucleus (Channel number from \'EDASP\')',
                          'Overwrite'],
                  types=['e', 'e', 'd', 'd', 'c'],
                  values=[curexpno, oexpno, Flist, Flist, ''],
                  comments=['', '', '', '', ''])


# Sanitize
nuc = int(nuc[1])
acquns_file = f"acqu{nuc+1}s"
procns_file = f"proc{nuc+1}s"
corr_nuc = int(corr_nuc[1])


# see if overwriting is allowed
if 'selected' in overwrite or overwrite:
    overwrite = True
else:
    overwrite = False


indir = os.path.join(curdir, iexpno)
outdir = os.path.join(curdir, oexpno)


# read the data
dic, data = ng.bruker.read(indir, read_acqus=True, read_pulseprogram=False)

print(acquns_file, procns_file, corr_nuc)
# change the processing frequency for appropriate dimension
dic[acquns_file]['NUC1'] = dic['acqus'][f'NUC{corr_nuc}']
dic[acquns_file]['SW'] *= dic[acquns_file]['BF1'] / dic['acqus'][f'BF{corr_nuc}']
dic[acquns_file]['BF1'] = dic['acqus'][f'BF{corr_nuc}']
dic[acquns_file]['O1'] = dic['acqus'][f'O{corr_nuc}']
dic[acquns_file]['SFO1'] = dic['acqus'][f'SFO{corr_nuc}']
dic[procns_file]['SF'] = dic['acqus'][f'SFO{corr_nuc}']


# write out the file
ng.bruker.write(outdir, dic, data, write_prog=False, write_acqus=True, 
                write_procs=True, pdata_folder=True, overwrite=overwrite)
