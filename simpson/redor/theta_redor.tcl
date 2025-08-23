spinsys {

    channels 1H 15N

    #---two spin
    nuclei 1H 15N
    dipole 1 2 3000 0 0 0

    #---alpha helix
    # nuclei 1H 15N 15N 15N 15N 15N
    # dipole 1 2 11000 62 42 112
    # dipole 1 3 704   48 166 188
    # dipole 1 4 306   173 141 294
    # dipole 1 5 238   221 117 184
    # dipole 1 6 185   18 91 88

    #---beta sheet
    # nuclei 1H 15N 15N 15N 15N 15N
    # dipole 1 2 11000 121 46 9
    # dipole 1 3 217   34 79 303
    # dipole 1 4 171   214 76 81
    # dipole 1 5 160   102 111 234
    # dipole 1 6 105   83 112 176

}

par {
    proton_frequency 700e6
    spin_rate        1e6/18
    sw               spin_rate
    np               64
    crystal_file     zcw376
    gamma_angles     18
    start_operator   I1x
    detect_operator  I1p
    method           taylor
    verbose          0100
    num_cores	     4
    variable rf      60e3
    variable theta   90
    variable epsilon 0.25
}

proc pulseq {} {

    global par
    maxdt 0.2


    #---calculated parameters
    set t180  [expr 0.5e6 / $par(rf)]
    set tr    [expr 1.0e6 / $par(spin_rate)]
    set trc   [expr (1.00 * $tr) - (0.5 * $t180)]
    set qtr   [expr (0.25 * $tr) - (0.5 * $t180)]
    set ini   [expr ($par(epsilon) - 0.25) * $tr]
    set final [expr $tr - $ini]
    set rf2 [expr $par(rf) / 180.0 * $par(theta)]


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
    pulse $t180 $par(rf) x $rf2 x
    delay $trc
    store 2

    #---actual theta-redor starts
    reset
    delay $tr
    prop 2
    delay $tr
    acq

    reset $ini
    prop 1
    delay $final
    prop 2
    delay $final
    prop 3
    store 4

    reset
    delay $ini
    prop 4
    delay $ini
    acq

    for {set i 2} {$i < $par(np)} {incr i} {

        reset $ini
        prop 1
        prop 4
        prop 3
        store 4

        reset
        delay $ini
        prop 4
        delay $ini
        acq
    }
}

proc main {} {
    global par
    set f [fsimpson]
    fsave $f $par(name).fid
}
