# REDOR after cp-based filtering

spinsys {
    channels 1H 13C
    nuclei 1H 13C
    dipole 1 2 -5000 0 0 0
}

par {
    proton_frequency  700e6
    spin_rate         62500
    np                64
    crystal_file      zcw376
    gamma_angles      32
    sw                spin_rate
    start_operator    I1x+I2z
    detect_operator   I1p
    verbose           0000
    num_cores	      4
    method            taylor
    variable rf       100e3
    variable cpf_rfH  150e3
    variable cpf_rfC  87.5e3
    variable cpf_time 400
    variable cpr_rfH  150e3
    variable cpr_rfC  87.5e3
    variable cpr_time 400       

}

proc pulseq {} {

    global par
    maxdt 0.2

    if {$par(rf) < $par(spin_rate)} {
        puts stderr "ValueError: RF ($par(rf)) cannot be lower than the spin rate ($par(spin_rate)).\nUse DEDOR instead of REDOR if this is required."
        exit 1
    }

    #---calculated parameters
    set t180      [expr 0.5e6 / $par(rf)]
    set tr        [expr 1.0e6 / $par(spin_rate)]
    set trc       [expr (1.00 * $tr) - (0.5 * $t180)]
    set qtr       [expr (0.25 * $tr) - (0.5 * $t180)]
    set cpf_ntr   [expr int($par(cpf_time) / $tr)]
    set cpr_ntr   [expr int($par(cpr_time) / $tr)]
    set cpf_delta [expr fmod($par(cpf_time), $tr)]
    set cpr_delta [expr fmod($par(cpr_time), $tr)]
    set cp_delta  [expr fmod($par(cpf_time) + $par(cpr_time), $tr)]
    
    if {$cp_delta > $tr} {
        set cp_delta [expr $cp_delta - $tr]
    }


    #---transverse I2 magnetization to be selected after cp
    matrix set 1 operator I2x+I2y

    #---forward cp 
    reset [expr $tr - $cp_delta]
    pulse $cpf_delta $par(cpf_rfC) x $par(cpf_rfH) x
    store 1

    reset [expr -$cpr_delta]
    pulse $tr $par(cpf_rfC) x $par(cpf_rfH) x
    store 2

    reset [expr -$cpr_delta]
    prop 2 $cpf_ntr
    store 2

    reset
    delay [expr $tr - $cp_delta]
    prop 1
    prop 2
    store 2

    #---reverse cp
    reset [expr -$cpr_delta]
    pulse $cpr_delta $par(cpr_rfC) x $par(cpr_rfH) x
    store 3

    reset 
    pulse $tr $par(cpr_rfC) x $par(cpr_rfH) x
    store 4 

    reset
    prop 4 $cpr_ntr
    store 4

    reset [expr -$cpr_delta]
    prop 3
    prop 4
    store 4

    #---redor recoupling propagator
    reset
    delay $qtr
    pulse $t180 0 x $par(rf)  x
    delay $qtr
    delay $qtr
    pulse $t180 0 x $par(rf)  y
    delay $qtr
    store 6

    #---central block propagator
    reset
    delay $trc
    pulse $t180 $par(rf) x $par(rf) x
    delay $trc
    store 7

    #---cp redor starts
    reset
    prop 2
    filter 1
    prop 4
    prop 7
    acq

    for {set i 1} {$i < $par(np)} {incr i} {
        reset
        prop 6
        prop 7
        prop 6
        store 7

        reset
        prop 2
        filter 1
        prop 4 
        prop 7
        acq
    }


}

proc main {} {
    global par
    set f [fsimpson]
    fsave $f $par(name).fid
}