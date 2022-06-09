# REDOR: Mirror symmetric version
# central pi pulses on both channels
# both the central pi pulses can be selective

spinsys {
    channels 13C 1H
    nuclei 13C 1H
    dipole 1 2 -10000 0 0 0
}

par {
    proton_frequency 700e6
    spin_rate        62500
    sw               spin_rate
    np               64
    crystal_file     zcw376
    gamma_angles     32
    start_operator   I2x
    detect_operator  I1p
    method           taylor
    verbose          0100
    num_cores	     4
    variable rf      100e3
    variable cp_rfH  150e3
    variable cp_rfC  87.5e3
    variable cp_time 150   
}

proc pulseq {} {

    global par
    maxdt 0.2

    if {$par(rf) < $par(spin_rate)} {
        puts stderr "ValueError: RF ($par(rf)) cannot be lower than the spin rate ($par(spin_rate)).\nUse DEDOR instead of REDOR if this is required."
        exit 1
    }

    #---calculated parameters
    set t180     [expr 0.5e6 / $par(rf)]
    set tr       [expr 1.0e6 / $par(spin_rate)]
    set trc      [expr (1.00 * $tr) - (0.5 * $t180)]
    set qtr      [expr (0.25 * $tr) - (0.5 * $t180)]
    set cp_ntr   [expr int($par(cp_time) / $tr)]
    set cp_delta [expr fmod($par(cp_time), $tr)]

    #---cp block
    reset [expr $tr - $cp_delta]
    pulse $cp_delta $par(cp_rfC) x $par(cp_rfH) x
    store 1

    reset
    pulse $tr $par(cp_rfC) x $par(cp_rfH) x
    store 2

    #---full cp propagator
    reset
    delay [expr $tr - $cp_delta]
    prop 1
    prop 2 $cp_ntr
    store 3


    #---redor recoupling propagator
    reset
    delay $qtr
    pulse $t180 0 x $par(rf)  x
    delay $qtr
    delay $qtr
    pulse $t180 0 x $par(rf)  y
    delay $qtr
    store 4

    #---central block propagator
    reset
    delay $trc
    pulse $t180 $par(rf) x $par(rf) x
    delay $trc
    store 5

    #---cp redor starts
    reset
    prop 3
    prop 5
    acq

    for {set i 1} {$i < $par(np)} {incr i} {
        reset
        # for every point, first calculate
        # redor and then prepend cp before 
        # detection
        prop 4
        prop 5
        prop 4
        store 5

        reset
        prop 3 
        prop 5
        acq
    }
}

proc main {} {
    global par
    set f [fsimpson]
    fsave $f $par(name).fid
}