"""
calcpwl.py

Calculates power level in watts required for a RF or
a pulse length, given a reference power level
and a reference RF or pulse length. 


Bugs and suggestions
--------------------
kaustuberm@tifrh.res.in

"""
from sys import argv


def parse_args(args):
    """
    Parse arguments and return a dictionary
    containing necessary functions

    """
    if len(args) == 1:
        return {}

    elif  


def sanitize(value):
    """

    """
    try:
        value = float(value)
    except:
        raise ValueError("{} is not a valid input".format(value))

    return value


def get_conditions():
    ref_rf = INPUT_DIALOG(
            items=["Required Pulse Length [OR, Reference RF (Hz/kHz)]"],
        )

    ref_watts = INPUT_DIALOG(
            items=["Reference Power in Watts"],
        )

    required_rf = INPUT_DIALOG(
            items=["Reference Pulse Length [OR, Required RF (Hz/kHz)]"],
        )

    return sanitize(ref_rf[0]), sanitize(ref_watts[0]), sanitize(required_rf[0])



if __name__ == "__main__":

    ref_rf, ref_watts, required_rf = get_conditions()
    req_watts = ref_watts * (required_rf/ref_rf)**2
    msg = "The new power level is {} Watts".format(req_watts)

    MSG(msg)

