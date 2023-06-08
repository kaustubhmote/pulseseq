# indirectly referencing nuclei

# usage:
# if you want to reference 15N nucleus that is encoded in F1 dimension
# based on 1H nucleus that is encoded in F3 (direct) dimension
# Make sure that the SR value for 1H is set correctly, and
# type: "ref.py 15N 1 1H 3"

from sys import argv

relative = {
    "1H": 1.000000000,
    "2H": 0.153506088,
    "13C": 0.251449530,
    "15N": 0.101329118,
    "31P": 0.404808636,
}


to_nucleus = argv[1]
to_channel = argv[2]
from_nucleus = argv[3]
from_channel = argv[4]

sf_from = float(GETPAR("{} SF".format(from_channel)))
ratio = relative[to_nucleus] / relative[from_nucleus]
sf_to = ratio * sf_from
PUTPAR("{} SF".format(to_channel), str(sf_to))
