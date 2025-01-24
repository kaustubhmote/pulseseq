"""
preset - automatically fills in appropriate parameters for acquisition
    and processing in Bruker-Topspin

USAGE
preset
preset --option (eg. preset --shapes)
preset --acqu
preset --proc
preset --all


INSTALLATION
1. Copy (or symlink) the directory `preset.py` to the following directory:
<topspin_location>/exp/stan/nmr/py/user/
2. If you now type 'preset' on the command line within TopSpin,
this documentation should pop up.


DESCRIPTION
preset supports automatic filling of acquisition and processing parameters
based on a custom sytax in your pulse program

"""

from sys import argv, path
import os

PRESET_PATH = os.path.join(topspin_location(), "exp", "stan", "nmr", "py", "user")
FLAGS = []
CMDLIST = []


def main():
    global FLAGS, CMDLIST, PRESET_PATH
    FLAGS = [f.lower() for f in argv[1:]]

    path.append(PRESET_PATH)

    if flag("zero-powers"):
        zero_pwl()

    PYCODE = read_preset_cmds()

    if ("dry" in FLAGS) or ("--dry" in FLAGS):
        VIEWTEXT(text=PYCODE)

    else:
        exec(PYCODE)


try:
    from ConfigParser import SafeConfigParser
except ModuleNotFoundError:
    # this will only fail if Python 3 is used
    # but that error will be handled by the
    # check_jython() function
    pass


def topspin_error():
    errmsg = """
    This file is meant to be executed
    using Jython from within TopSpin
    Please see the doctring for more
    details.
    """
    return errmsg


def check_jython():
    """
    Checks whether Jython is being used to run this script
    from within TopSpin

    """
    # some of the functions defined in the global namespace
    # by TopSpin which are also used by xcpy
    topspin_inbuilts = ["MSG", "INPUT_DIALOG", "CURDATA"]

    g = globals().keys()
    for function in topspin_inbuilts:
        if function in g:
            pass
        else:
            raise Exception(topspin_error())
    return True


def topspin_location():
    """
    Gets TopSpin home directory. Also serves to check
    whether the script is being executed from within
    TopSpin or externally.

    """
    try:
        # topspin >= 3.6
        toppath = sys.getBaseProperties()["XWINNMRHOME"]
    except AttributeError:
        try:
            # topspin >= 3.1 and <= 3.5
            toppath = sys.registry["XWINNMRHOME"]
        except (AttributeError, KeyError):
            # topspin < 3.1
            toppath = sys.getEnviron()["XWINNMRHOME"]

    # if all the above fail, there should be an exception raised and
    # the function should not return anything
    return toppath


def flag(*names, **kwargs):
    """
    returns true if any of the items passed
    to the function are in global FLAGS

    Example
    -------

    if flag('--test'):
       print("test")

    In the above case, 'test' is printed
    out if the script is run with 'preset --test'

    """
    global FLAGS

    try:
        if kwargs["restrict"]:
            if _check_flags_and_return(names):
                return True
        else:
            if _check_flags_and_return(names, ["all", "--all"]):
                return True

    except KeyError:
        if _check_flags_and_return(names, ["all", "--all"]):
            return True

    return False


def _check_flags_and_return(names, extra_conditions=None):
    global FLAGS

    if extra_conditions is None:
        extra_conditions = []

    for name in names:
        for f in FLAGS:
            if any([f in extra_conditions, f == name, f == "--" + name]):
                return True

    return False


def run(*cmds):
    """
    runs command or a list/tuple of commands
    in topspin

    """
    for cmd in cmds:
        if isinstance(cmd, (list, tuple)):
            for c in cmd:
                XCMD(str(c))
        else:
            XCMD(str(cmd))


def pprint(*args):
    """
    A simple wrapper around the MSG utility

    Parameters
    ----------
    val : any
        anything that can be converted to a string
    """
    message = ", ".join([str(a) for a in args])

    MSG(message)


def read_preset_cmds(ppdir=None, ppname=None):
    """
    Reads the python section of the pulse program

    Returns
    -------
    pycode : str
        the python code to be executed
    """

    import re

    top = topspin_location()

    if ppdir is None:
        ppdir = top + "/exp/stan/nmr/lists/pp/user/"

    if ppname is None:
        ppname = get("PULPROG")

    pprg = ppdir + ppname

    try:
        with open(pprg, "r") as f:
            pprg_full = f.read()

    except IOError as e:
        try:
            ppdir = "/home/kaustubh/data/repositories/pulseseq/pp/"
            pprg = ppdir + ppname

            with open(pprg, "r") as f:
                pprg_full = f.read()

        except IOError as e:
            ppname, ppdir = input_dialog(
                ["name", "pp directory"], [ppname, ppdir], header=str(e)
            )

        return read_preset_cmds(ppdir, ppname)

    parsed = [list(i) for i in re.findall(r">>>((.|\n)*?)<<<", pprg_full)]
    for p in parsed:
        p[0] = p[0].strip()

    pycode = "\n".join([line for item in parsed for line in item])

    return pycode


def get_rfs():
    """
    generate a rf table based on the values of
    p1 p2 p3 and plw1 plw2 plw3 (HCN)

    """
    from collections import namedtuple

    pars = namedtuple("pars", ["nutation", "p90", "watts"])

    rf_table = {}
    for n, v in zip("HCN", "123"):
        p = get_pulse(v)
        plw = get_power(v)
        rf = 250e3 / p
        rf_table[n] = pars(rf, p, plw)
    return rf_table


def read_rftable():
    import pickle

    cd = CURDATA()
    curdir = os.path.join(cd[3], cd[0])

    try:
        fpath = os.path.join(curdir, "rftable")
        pprint(fpath)
        return pickle.loads(fpath)

    except IOError:
        return dict()


def get(name, axis=0, dtype=None):
    """
    retrieves parameters and
    converts to appropriate types

    """
    val = GETPAR(name, axis=axis)

    if dtype:
        return dtype(val)
    else:
        return val


def get_constant(name):
    return get("CNST {}".format(name), dtype=float)


def get_pulse(name):
    return get("P {}".format(name), dtype=float)


def get_power(name):
    return get("PLW {}".format(name), dtype=float)


def get_counter(name):
    return get("L {}".format(name), dtype=int)


def setpar(name, value):
    """
    sets the parameter to the given value

    """
    global CMDLIST, FLAGS

    if "TABLE" in FLAGS:
        CMDLIST.append((name, value))

    elif "CONFIRM" in FLAGS:
        value = input_dialog(
            names=[str(name)],
            values=[str(value)],
            header="Should this be set?",
        )
        PUTPAR(name, "{}".format(value))

    else:
        PUTPAR(name, "{}".format(value))


def rf_to_pwl(rfhz, rftable):
    """
    converts nutation frequency to pwl in watts
    based on te main table

    """
    return (rfhz / rftable.nutation) ** 2 * rftable.watts


def rf_to_plen(rfhz, rftable, angle):
    """
    gets the pulse length

    """
    return (rftable.nutation / rfhz) ** 0.5 * (rftable.p90 * angle / 90.0)


def input_dialog(names, values=[], header="", allfloat=False):
    if type(names) == str:
        names = [names]

    ln, lv = len(names), len(values)

    if lv > ln:
        values = values[:ln]
    elif lv < ln:
        for i in range(lv - ln):
            values.append("")

    result = INPUT_DIALOG(
        header,
        header=header,
        items=names,
        values=values,
        comments=[""] * ln,
        types=["1"] * ln,
        buttons=["Execute", "Cancel"],
        columns=20,
    )

    if allfloat:
        return [float(i) for i in result]
    else:
        return result


def single_input(name, value=None, dtype=float):
    out = input_dialog([name], [value], allfloat=False)
    return dtype(out[0])


def zero_pwl():
    for i in range(64):
        setpar("PLW {}".format(i), 0)
        setpar("SPW {}".format(i), 0)


if __name__ == "__main__":
    main()
