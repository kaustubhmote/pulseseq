# pisema with fslg decoupling


spinsys {
    channels 15N 1H
    nuclei 15N 1H
    dipole 1 2 10000 0 0 0
}

par {
    proton_frequency 700e6
    spin_rate        0
    rotor_angle      0
    crystal_file     alpha0beta0
    np               2048
    start_operator   I2x-I1y
    detect_operator  I2p
    method           taylor
    verbose          0100
    num_cores	     1
    variable rf      50e3
    variable cp_time 150
    variable pi      acos(-1)
    variable tm      atan(sqrt(2.0))*180.0/pi
    variable theta   90-tm 
    sw               rf/sqrt(2.0/3.0)/2
}

proc pulseq {} {

    global par

    set tth [expr 1e6 * $par(theta) / 360 / $par(rf)]
    set off [expr -sqrt(0.5) * $par(rf)]
    set rf2 [expr  sqrt(1.5) * $par(rf)]
    set tp  [expr 1e6 * sqrt(2.0/3.0) / $par(rf)]

    reset
    offset $off 0
    pulse $tp $par(rf) y $rf2 x
    offset [expr -$off] 0
    pulse $tp $par(rf) -y $rf2 -x
    offset 0 0
    store 1

    reset
    pulseid $tth $par(rf) -x 0 x
    store 2
    turnoff dipole_1_2
    acq

    for {set i 1} {$i < $par(np)} {incr i} {
        reset
        prop 2 
        prop 1
        store 2
        turnoff dipole_1_2
        acq
    }

    

}

proc main {} {
    global par
    set f [fsimpson]
    fzerofill $f 4096
    faddlb $f 20 1
    fft $f 
    fsave $f $par(name).spe
}