# PULSESEQ
NMR pulse sequences (`pp_solids` and `pp_solution`), decoupling sequences (`cpd`), shape pulses (`wave`), AU (`au`) and Python (`python`) programs for Bruker spectrometers.

## Requirements
All of the pulse-sequences given here have been implemented on spectrometers with Avance III console and TopSpin version >= 2.1
Each pulse-sequence will have the TopSpin software version where it was tested

## Installation
You can download this repository with `git clone https://github.com/kaustubhmote/pulseseq.git`. Unpack the contents in their respective places in the topspin directory:
- `pp_solids` and `pp_solution` : TOPSPIN_FOLDER/exp/stan/nmr/lists/pp/user
- `wave` : TOPSPIN_FOLDER/exp/stan/nmr/lists/wave/user
- `au` : TOPSPIN_FOLDER/exp/stan/nmr/au/src/user
- `cpd`: TOPSPIN_FOLDER/exp/stan/nmr/lists/cpd/user

Alternatively, you can specify the folders to use directly from Topspin


## Python Programs
Symlink or copy the following folders/files to the specified places
- `python/xcpy.py` : TOPSPIN_FOLDER/exp/stan/nmr/py/user/xcpy.py
- `python/cpython` : TOPSPIN_FOLDER/exp/stan/nmr/py/user/cpython 
Edit the `xcpy.py` file to specify the (c)python that you want to use using
the instructions in that file.


