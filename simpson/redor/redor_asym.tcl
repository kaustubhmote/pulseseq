# REDOR: Mirror asymmetric version
# central pi pulses on a single channel

spinsys {
    channels 13C 1H
    nuclei 13C 1H
    dipole 1 2 -5000 0 0 0
}

par {
    proton_frequency 700e6
    spin_rate        62500
    sw               spin_rate
    np               100
    crystal_file     zcw376
    gamma_angles     32
    start_operator   I1x
    detect_operator  I1p
    method           taylor
    verbose          0100
    num_cores	     1
    variable rf      100e3
}

proc pulseq {} {

    global par
    maxdt 0.2

    if {$par(rf) < $par(spin_rate)} {
        puts stderr "ValueError: RF ($par(rf)) cannot be lower than the spin rate ($par(spin_rate)).\nUse DEDOR instead of REDOR if this is required."
        exit 1
    }

    #---calculated parameters
    set t180  [expr 0.5e6 / $par(rf)]
    set tr    [expr 1.0e6 / $par(spin_rate)]
    set trc   [expr (1.00 * $tr) - (0.5 * $t180)]
    set qtr   [expr (0.25 * $tr) - (0.5 * $t180)]

    #---redor recoupling left block propagator
    reset
    delay $qtr
    delay $qtr
    pulse $t180 0 x $par(rf)  x
    delay $qtr
    delay $qtr
    pulse $t180 0 x $par(rf)  y
    store 1

    #---central block propagator
    reset
    delay $trc
    pulse $t180 $par(rf) x 0 x
    delay $trc
    store 2


    #---actual REDOR starts
    reset
    prop 2
    acq
    store 2 

    for {set i 1} {$i < $par(np)} {incr i} {
        prop 1
        prop 2
        prop 1
        acq
        store 2
    }
}

proc main {} {
    global par
    set f [fsimpson]
    fsave $f $par(name).fid
}