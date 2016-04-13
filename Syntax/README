If you use vim to edit pulse-sequences on bruker, this directory contains a syntax file and
a coloring scheme that will work with bruker file

bruker.vim is a vim syntax file for bruker
This is not complete and definitely needs work
Add bruker.vim to your vim syntax directory 

bruker-colors.vim is a color scheme on a dark background in vim for looking at the pulse sequence
Its basically the 'neverland' color scheme with some modifications. This needs to go in your vim colors directory
Add the following lines to your .vimrc (my extensions are .pseq)

################################################
"bruker file type
au BufNewFile,BufRead *.pseq setlocal ft=bruker
au BufNewFile,BufRead pulseprogram setlocal ft=bruker
autocmd FileType bruker colorscheme neverland
################################################

An Example of the sequence looks in vim
!(vim_example.png?raw=true "Bruker pulse sequence in vim")

