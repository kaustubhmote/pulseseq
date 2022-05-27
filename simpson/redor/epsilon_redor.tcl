spinsys {
    channels 13C 1H
    nuclei 13C 1H
    dipole 1 2 -5000 0 39 0
}

par {
    proton_frequency 700e6
    spin_rate        62500
    sw               31250
    np               30
    crystal_file     zcw143
    gamma_angles     12
    start_operator   I1x
    detect_operator  I1p
    variable rf      100e3
    verbose          0100
    num_cores	     4
    variable epsilon 0.25
}

proc pulseq {} {
    global par

    maxdt 1.0

    set t180  [expr 0.5e6 / $par(rf)]
    set tr    [expr 1.0e6 / $par(spin_rate)]
    set trc   [expr (1.00 * $tr) - (0.5 * $t180)]
    set qtr   [expr (0.25 * $tr) - (0.5 * $t180)]
    set ini   [expr $par(epsilon - 0.25) * $tr]
    set final [expr $tr - $ini]

    reset
    delay $trc
    pulse $t180 $par(rf) x $par(rf) x
    delay $trc
    store 2

    reset
    for {set i 0} {$i < $par(np)} {incr i} {
        reset

        delay $ini
        for {set j 0} {$j<$i} {incr j} {
            delay $qtr
            pulse $t180 0 x $par(rf)  x
            delay $qtr
            delay $qtr
            pulse $t180 0 x $par(rf)  y
            delay $qtr

        }

        delay $final
        prop 2
        delay $final

        for {set j 0} {$j<$i} {incr j} {
            delay $qtr
            pulse $t180 0 x $par(rf)  y
            delay $qtr
            delay $qtr
            pulse $t180 0 x $par(rf)  x
            delay $qtr
        }
        delay $ini
        acq
    }
}

proc main {} {
    global par
    set f [fsimpson]
    fsave $f $par(name).fid
}


