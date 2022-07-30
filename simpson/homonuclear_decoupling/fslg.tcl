# fslg decoupling


spinsys {
    channels 1H
    nuclei 1H
}

par {
    proton_frequency 700e6
    spin_rate        0
    rotor_angle      0
    crystal_file     alpha0beta0
    np               512
    start_operator   I1z
    detect_operator  I1x I1y I1z
    method           taylor
    verbose          0100
    num_cores	     1
    variable rf      50e3
    variable pi      acos(-1)
    variable tm      atan(sqrt(2.0))*180.0/pi
    sw               10e3
    conjugate_fid    true
}

proc pulseq {} {

    global par
    set off [expr -sqrt(0.5) * $par(rf)]
    set tp  [expr 1e6 * sqrt(2.0/3.0) / $par(rf)]


    reset
    offset $off
    acq_block {
        pulse $tp $par(rf) y
    }
    

}

proc main {} {
    global par
    set f [fsimpson]
    fsave $f $par(name).fid
}