"""
Estimate temparature from spinning frequency for different rotors

Based on:
Purusottam et al., J Magn Reson (2014), 246, 69-71

Should be considered as approximate. For most protein samples, use 
the water chemical shift as the more accurate marker

"""
from __future__ import division
import sys


def main():

    rotor = sys.argv[1].split("m")[0]
    rotor = float(rotor)

    frequency = sys.argv[2]
    if frequency.endswith("k"):
        f = frequency.split("k")[0]
        f = float(f)
    else:
        f = float(frequency) / 1e3
        
    rise = temperature_rise(rotor, f)

    msg = "Spinning a {:.1f} mm rotor at {:.3f} kHz raises the temperature by  approx. {:.0f} K".format(
        rotor, f, rise,
    )

    try:
        MSG(msg)
    except NameError:
        print(msg)


def temperature_rise(rotor, frequency):

    if abs(rotor - 4.0) < 1e-3:
        return 0.1056 * frequency ** 2 - 0.1738 * frequency

    elif abs(rotor - 3.2) < 1e-3:
        return 0.0853 * frequency ** 2 - 0.2337 * frequency

    elif abs(rotor - 2.5) < 1e-3:
        return 0.0544 * frequency ** 2 - 0.0585 * frequency

    elif abs(rotor - 1.3) < 1e-3:
        return 0.0108 * frequency ** 2 - 0.1859 * frequency

    else:
        MSG("Dont have data for a {} mm rotor ".format(rotor))
        raise ValueError("Dont have data for a {} mm rotor ".format(rotor))


if __name__ == "__main__":
    main()
