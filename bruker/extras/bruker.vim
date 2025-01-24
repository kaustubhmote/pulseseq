" Vim syntax file
" Language: Bruker Pulse Program
" Maintainer: Kaustubh R. Mote
" Last Change:  
" Credits:      

if exists("b:current_syntax")
  finish
endif

syntax keyword brukStatement      lo to times goto
syntax keyword brukStatement      go gonp goscnp eosc eoscnp rcyc adc
syntax keyword brukStatement      go1 go2 gonp1 gonp2 eoscnp1 eoscnp2 rcyc1 rcyc2 
syntax keyword brukStatement      ze zd wr if wr1 wr2 ze1 zd1 ze2 zd2 mc 
syntax keyword brukStatement      else ifdef endif 
syntax keyword brukStatement      rf rf1 rf2 ifp dfp rfp 
syntax keyword brukStatement      aqseq F1QF F1PH F1EA F0 F1I F2I F2QF F2PH F2EA
syntax keyword brukStatement      calph caldel calgrad calclc calclist calphptr
syntax keyword brukStatement      STARTADC RESETPHASE sample RG_ON
syntax keyword brukStatement      st st0 
syntax keyword brukStatement      STARTADC2 RESETPHASE2 sample2 RG_ON2 
syntax keyword brukStatement      vpidx res inc dec idx currentpower 
syntax keyword brukStatement      larger max random 
syntax keyword brukStatement      center ralign lalign refalign
syntax keyword brukStatement      suspend autosuspend calcsuspend calcautosuspend
syntax keyword brukStatement      stop_calc resume_calc
syntax keyword brukStatement      exec_on_chan exec_on_other exec_wait 
syntax keyword brukStatement      exec_enable free_chan
syntax keyword brukStatement      spincnt_use store_spinrate_d spincnt_measure
syntax keyword brukStatement      spincnt_start spincnt_wait
syntax keyword brukStatement      rcen anavpt
syntax keyword brukStatement      do cw fq hd groff finally
syntax match brukStatement        "\vf[1-9]"
syntax match brukStatement        "\v(i|d|r)pu([0-9]|[1-5][0-9]|[6][0-4])+" 
syntax match brukStatement        "\v(i|d|r)(p|pp)([0-9]|[1-5][0-9]|[6][0-4])+"
syntax match brukStatement        "\v(i|d|r)d([0-9]|[1-5][0-9]|[6][0-4])+"
syntax match brukStatement        "\viu([0-9]|[1-5][0-9]|[6][0-4])+"
syntax match brukStatement        "\vcpd(s*|hd*|ngs*)([0-8])+"
highlight link brukStatement      Statement

syntax match brukComment          "\v; #.*$"
syntax match brukComment          "\v; .*$"
syntax match brukComment          "\v(/\*)(.|\n)*(\*\\)"
highlight link brukComment        Comment

syn match brukPulsepars "\v(\s*|;*|s*|m*|u*|(\sv)*)p([0-9]|[1-5][0-9]|[6][0-3])+" 
syn match brukPulsepars "\v(\s*|;*|^*)ph(\=|[0-9]|[1-2][0-9]|[3][0,1])+"
syn match brukPulsepars "\v(\s|;)pl([0-9]|[1-5][0-9]|[6][0-3])+"
syn match brukPulsepars "\v(\s|;)plw([0-9]|[1-5][0-9]|[6][0-3])+"
syn match brukPulsepars "\v(\s|;|:)sp([0-9]|[1-5][0-9]|[6][0-3])+"
syn match brukPulsepars "\v(\s|;)spf([0-9]|[1-2][0-9]|[3][0,1])+"
syn match brukPulsepars "\v(\s|;)pcpd([0-9]|[1-2][0-9]|[3][0,1])+"
syn match brukPulsepars "\vgron(|[0-9]|[1-2][0-9]|[3][0,1])+"
highlight link brukPulsepars Special

syn match brukDelays "\v(\s*|;*)d([0-9]|[1-5][0-9]|[6][0-4])+"
syn match brukDelays "\v[-+]?[0-9]*\.?[0-9]+(u|m|s)"
syn match brukDelays "\vin([0-9]|[1-5][0-9]|[6][0-4])+"
syn match brukDelays "\v(i*|d*|r*)vd(idx*)"
syn keyword brukDelays aq acqt0 dw de de1 depa derx deadc 
syn keyword brukDelays inf1 inf2 inf3 inf4 inf5 inf6
highlight link brukDelays SpecialKey 

syn match brukConstants "\v(\s*|;*)cnst([0-9]|[1-2][0-9]|[3][0,1])+"
syn match brukConstants "\v(\s|;|\"|\/)l([0-9]|[1-2][0-9]|[3][0,1])+"
syn keyword brukConstants td1 td2 td3 td4 td5 td6 nsdone
highlight link brukConstants Constant

syn match brukFunction "\vdefine\s(list|loopcounter|pulse|delay\s)"
syn match brukFunction "\v#(define|ifdef|endif|ifndef)" 
syn match brukFunction  '\v([''"])(.{-})\1'
highlight link brukFunction Function



