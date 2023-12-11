# indirectly referencing nuclei
help = """
Usage:
If you want to reference 15N nucleus that is encoded in F1 dimension
based on 1H nucleus that is encoded in F2 (direct) dimension
Make sure that the SR value for 1H is set correctly, and
type: 'ref.py 15N 1 1H 2'

"""
from sys import argv

def main():
    if (len(argv) != 5) or ("help" in argv[1]):
        MSG(help)
    else:
        to_nucleus, to_channel, from_nucleus, from_channel = argv[1:]
        indirect_reference(to_nucleus, to_channel, from_nucleus, from_channel)

def indirect_reference(to_nucleus, to_channel, from_nucleus, from_channel):
    sf_from = float(GETPAR("{} SF".format(from_channel)))
    ratio = RELATIVE[to_nucleus] / RELATIVE[from_nucleus]
    sf_to = ratio * sf_from
    PUTPAR("{} SF".format(to_channel), str(sf_to))

RELATIVE = {
    "1H": 1.000000000,
    "2H": 0.153506088,
    "13C": 0.251449530,
    "15N": 0.101329118,
    "31P": 0.404808636,
}

if __name__ == "__main__":
    main()
