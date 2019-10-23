"""
Estimate Temparature from water peak

"""
import sys


def temp_from_ppm(delta):
    """
    Calculates temperature from given chemical shift

    >>> from watertemp import temp_from_ppm
    >>> temp_from_ppm(4.7)
    32.0
    >>> temp_from_ppm(5.5)
    -40.0

    """
    return 455 - (90 * delta)


def ppm_from_temp(temperature):
    """
    Calculates chemical shift from give temperature

    >>> from watertemp import ppm_from_temp
    >>> ppm_from_temp(32.0)
    4.7
    >>> ppm_from_temp(-30)
    5.388888888888889
    >>> 
 
    """
    return (455 - temperature) / 90


def parse(input_string):
    """
    Parses an input string to give either the 
    temperature or the chemical shifts


    >>> from watertemp import parse
    >>> parse("273k")
    -0.14999999999997726
    >>> parse("273K")
    -0.14999999999997726
    >>> parse("10C")
    10.0
    >>> parse("10c")
    10.0
    >>> parse("4.3p")
    4.3
    >>> parse("4.3P")
    """
    units = input_string[-1].lower()

    if units == "k":
      value = float(input_string[:-1]) - 273.15
    elif units == "c":
      value = float(input_string[:-1])
    elif units == "p":
      value = float(input_string[:-1])

    return value


if __name__ == "__main__":

    value = sys.argv[1]
    units = value[-1]
    
    if units.lower() in ("k", "c"):
        temperature = parse(value)
        out = ppm_from_temp(temperature)
        msg = 'At {:.2f} Celcius, the chemical shift of water will be {:.2f} ppm'.format(temperature, out)

    elif units.lower() == "p":
        delta = parse(value)
        out = temp_from_ppm(delta)
        msg = 'When water is at {:.2f} ppm, the sample temperature is estimated to be {:.2f} Celcius'.format(delta, out)

    try:
        MSG(msg)
    except:
        print(msg)

