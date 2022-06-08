# ε-DIPSHIFT
# M. G. Jain et al., J. Phys. Chem. B 124, 1444 (2020).
# 1. rf: nutation for the recoupling pulses
# 2. ntr: 1/2 * number of rotor blocks for applying the recoupling pulses
# 3. half: 0 if the entire dipshift profile is to be acquired, 1 if half is to be acquired.

spinsys {
    channels 13C 1H
    nuclei 13C 1H
    dipole 1 2 -5000 0 0 0
}

par {
    proton_frequency 700e6
    spin_rate        62500
    sw               spin_rate
    np               32
    crystal_file     zcw376
    gamma_angles     32
    start_operator   I1x
    detect_operator  I1p
    verbose          0100
    num_cores	     4
    variable rf      100e3
    variable ntr     16
    variable half    0
}

proc pulseq {} {

    global par
    maxdt 0.2

    #---check if parameters are sensible
    if {$par(rf) < $par(spin_rate)} {
        puts stderr "ValueError: RF ($par(rf)) cannot be lower than the spin rate ($par(spin_rate)).\nUse DE-DIPSHIFT instead of DIPSHIFT if this is required."
        exit 1
    }

    #---calculated parameters
    set t180  [expr 0.5e6 / $par(rf)]
    set tr    [expr 1.0e6 / $par(spin_rate)]
    set trc   [expr (1.00 * $tr) - (0.5 * $t180)]
    set qtr   [expr (0.25 * $tr) - (0.5 * $t180)]

    #---calculate difference in scaling between points
    if {$par(half) == 0} {
        set delta [expr 0.50 / ($par(np) - 1)]
    } else {
        set delta [expr 0.25 / ($par(np) - 1)]
    }

    #--- a new loop for each point on the dipshift curve
    for {set i 1} {$i <= $par(np)} {incr i}  {
        reset

        #---caculate scaling for this point
        set epsilon [expr ($i - 1) * $delta + 0.5]
        set ini   [expr ($epsilon - 0.25) * $tr]
        set final [expr $tr - $ini]

        #---recoupling left block propagator
        reset $ini
        delay $qtr
        pulse $t180 0 x $par(rf)  x
        delay $qtr
        delay $qtr
        pulse $t180 0 x $par(rf)  y
        delay $qtr
        store 1

        #---recoupling right block propagator
        reset $final
        delay $qtr
        pulse $t180 0 x $par(rf)  x
        delay $qtr
        delay $qtr
        pulse $t180 0 x $par(rf)  y
        delay $qtr
        store 3

        #---central block propagator
        reset
        delay $trc
        pulse $t180 $par(rf) x $par(rf) x
        delay $trc
        store 2

        #---actual epsilon DIPSHIFT starts
        reset
        delay $ini
        prop 1 $par(ntr)
        delay $final
        prop 2
        delay $final
        prop 3 $par(ntr)
        delay $ini
        acq
    }

}

proc main {} {
    global par
    set f [fsimpson]
    fsave $f $par(name).fid
}