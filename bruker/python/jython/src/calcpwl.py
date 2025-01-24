"""
calcpwl.py

Calculates power level in watts required for a RF or
a pulse length, given a reference power level
and a reference RF or pulse length. 


Bugs and suggestions
--------------------
krmote@tifrh.res.in

"""

def parse_args(args):
    """
    Parse arguments and return a dictionary
    containing necessary functions

    """
    if len(args) == 1:
        return {}


def sanitize(value):
    """

    """
    try:
        value = float(value)
    except:
        raise ValueError("{} is not a valid input".format(value))

    return value


def get_conditions():
    ref_rf = INPUT_DIALOG(items=["Required Pulse Length [OR, Reference RF (Hz/kHz)]"],)
    ref_rf = sanitize(ref_rf[0])

    ref_watts = INPUT_DIALOG(items=["Reference Power in Watts"],)
    ref_watts = sanitize(ref_watts[0])

    required_rf = INPUT_DIALOG(
        items=["Reference Pulse Length [OR, Required RF (Hz/kHz)]"],
    )
    required_rf = sanitize(required_rf[0])

    return ref_rf, ref_watts, required_rf


if __name__ == "__main__":

    ref_rf, ref_watts, required_rf = get_conditions()
    req_watts = ref_watts * (required_rf / ref_rf) ** 2
    msg = "The new power level is {} Watts".format(req_watts)

    MSG(msg)
