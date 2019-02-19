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
iexpno, oexpno, f1_nucleus, f1_sfo, overwrite = dialog(
                  header='Rectify F1 dimension parameters',
                  info='Correct the parameters for the F1 dimension',
                  labels=['Processed dataset number to correct',
                          'PROCNO for the output data',
                          'New F1 Nucleus',
                          'New F1 Spectrometer Frequency (SFO)',
                          'Overwrite'],
                  types=['e', 'e', 'e', 'e', 'c'],
                  values=[curexpno, oexpno, '', '', ''],
                  comments=['', '', '', '', ''])


indir = os.path.join(curdir, iexpno)
outdir = os.path.join(curdir, oexpno)

# read the data
dic, data = ng.bruker.read(indir, read_acqus=True)


# change the processing frequency for F1 dimension
dic['acqu2s']['NUC1'] = dic['acqus']['NUC3']
dic['acqu2s']['BF1'] = dic['acqus']['BF3']
dic['acqu2s']['O1'] = dic['acqus']['O3']
dic['acqu2s']['SFO1'] = dic['acqus']['SFO3']
dic['acqu2s']['SW'] *= dic['acqus']['BF1'] / dic['acqus']['BF3']
dic['proc2s']['SF'] = dic['acqus']['SFO3']

ng.bruker.write(outdir, dic, data, write_prog=False, write_acqus=True, 
                write_procs=True, pdata_folder=True)
