# PULSESEQ
NMR pulse sequences (`pp_solids` and `pp_solution`), decoupling sequences (`cpd`), shape pulses (`wave`), AU (`au`) and Python (`python`) programs for Bruker spectrometers.
These are compatible with Topspin 3.5 and above and tested with Avance III and above.

## Requirements
All of the pulse-sequences given here have been implemented on spectrometers with Avance III console 
and TopSpin version >= 2.1. Each pulse-sequence will have the TopSpin software version where it was tested

## Installation
You can download this repository with `git clone https://github.com/kaustubhmote/pulseseq.git`. 
Unpack the contents in their respective places in the topspin directory:
- `pp_solids` and `pp_solution` : TOPSPIN_FOLDER/exp/stan/nmr/lists/pp/user
- `wave` : TOPSPIN_FOLDER/exp/stan/nmr/lists/wave/user
- `au` : TOPSPIN_FOLDER/exp/stan/nmr/au/src/user
- `cpd`: TOPSPIN_FOLDER/exp/stan/nmr/lists/cpd/user
Alternatively, you can specify the folders to use directly from Topspin


## Python Programs
This is a small collection of Cpython and Jython scripts that can be executed from within Topspin 
using using the [xcpy](https://github.com/jjhelmus/nmrglue/blob/master/nmrglue/util/xcpy.py) utility available in nmrglue (v 0.8-dev and later), or as standalone scripts 
from the command line.

- Requirements
1. Installation instructions for `xcpy.py` are available [here](https://github.com/jjhelmus/nmrglue/blob/master/nmrglue/util/xcpy.py)
2. Scripts within `python/topspin` directory are meant to be run via Topspin. 
2. The following is a superset of dependencies for scripts within `cpython`: 
   - (c)python 3.7 and above
   - numpy
   - scipy
   - matplotlib
   - nmrglue v0.8-dev 
