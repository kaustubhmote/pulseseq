# ε-REDOR
# M. G. Jain et al., J. Chem. Phys. 150, 134201 (2019).
# 1. rf: nutation for the recoupling pulses
# 2. epsilon: scaling = sin(2*π*ε)

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
    num_cores	     1
    variable rf      100e3
    variable epsilon 0.25
}

proc pulseq {} {

    global par
    maxdt 0.2

    #---verify global parameters
    if {$par(epsilon) < 0.25} {
        puts stderr "ValueError: epsilon cannot take values less than 0.25.\nCurrently it is set to $par(epsilon)"
        exit 1
    }

    if {$par(rf) < $par(spin_rate)} {
        puts stderr "ValueError: RF ($par(rf)) cannot be lower than the spin rate ($par(spin_rate)).\nUse DEDOR instead of REDOR if this is required."
        exit 1
    }

    #---calculated parameters
    set t180  [expr 0.5e6 / $par(rf)]
    set tr    [expr 1.0e6 / $par(spin_rate)]
    set trc   [expr (1.00 * $tr) - (0.5 * $t180)]
    set qtr   [expr (0.25 * $tr) - (0.5 * $t180)]
    set ini   [expr ($par(epsilon) - 0.25) * $tr]
    set final [expr $tr - $ini]

    #---redor recoupling left block propagator
    reset $ini
    delay $qtr
    pulse $t180 0 x $par(rf)  x
    delay $qtr
    delay $qtr
    pulse $t180 0 x $par(rf)  y
    delay $qtr
    store 1

    #---redor recouplign right block propagator
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

    #---actual epsilon_REDOR starts
    for {set i 0} {$i < $par(np)} {incr i} {
        reset
        delay $ini
        prop 1 $i
        delay $final
        prop 2
        delay $final
        prop 3 $i
        delay $ini
        acq
    }
}

proc main {} {
    global par
    set f [fsimpson]
    fsave $f $par(name).fid
}