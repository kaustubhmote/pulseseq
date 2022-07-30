# REDOR: Mirror asymmetric version
# central pi pulses on a single channel

spinsys {
    channels 1H 13C
    nuclei 1H 13C
    dipole 1 2 -10000 0 0 0
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
    method           taylor
    verbose          0100
    num_cores	     4
    variable rf      100e3
}

proc pulseq {} {

    global par
    maxdt 0.2

    if {$par(rf) < $par(spin_rate)} {
        puts stderr "ValueError: RF ($par(rf)) cannot be lower than the spin rate ($par(spin_rate)).\nUse DEDOR instead of REDOR if this is required."
        exit 1
    }

    matrix set 10 operator I1y*I2z
    # putmatrix [matrix get 1]
    # puts "--------"


    #---calculated parameters
    set t180  [expr 0.50e6 / $par(rf)]
    set t90   [expr 0.25e6 / $par(rf)]
    set tr    [expr 1.0e6 / $par(spin_rate)]
    set trc   [expr (1.00 * $tr) - (0.5 * $t180)]
    set qtr   [expr (0.25 * $tr) - (0.5 * $t180)]
    set delta [expr $tr - 3 * $t90]

    #---redor recoupling left block propagator
    reset
    delay $qtr
    pulse $t180 0 x $par(rf)  x
    delay $qtr
    delay $qtr
    pulse $t180 0 x $par(rf)  y
    delay $qtr
    store 1

    reset
    acq

    reset
    prop 1
    store 2
    acq

    for {set i 2} {$i < $par(np)} {incr i} {
        reset
        prop 1
        prop 2
        store 2

        reset
        prop 2
        filter 10
        prop 2
        acq
    }
}

proc main {} {
    global par
    set f [fsimpson]
    fsave $f $par(name).fid
}