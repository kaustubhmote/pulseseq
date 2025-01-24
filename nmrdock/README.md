# NMRDock

A Dockerfile to build a containerized version of NMRPipe. Based on the Dockerfile available in the https://github.com/compbiocore/nmrdock. Adapted for Ubuntu22.04 and tested with the latest available version of NMRPipe (11.7 Rev 2024.039.18.43 64-bit)


## How to build

### Requirements

You will need `Docker` installed. Instructions for this can be found here: [https://docs.docker.com/get-started/get-docker/](https://docs.docker.com/get-started/get-docker/).


### 1. Download NMRPipe installers

If you have `curl` available, then do run the following commands. They will fetch all the required files from https://www.ibbr.umd.edu/nmrpipe/install.html. Please note that this is an ~670 MB download. 

```bash
$ cd nmrdock
$ ./download-nmrpipe 
```

Else, you can manually download all the files from the above website. Put these files in a folder called `nmrpipe` inside `nmrdock`. 

There should be a total of 7 files: `install.com`, `binval.com`, `NMRPipeX.tZ`, `dyn.tZ`, `plugin.smile.tZ`, `s.tZ`, and `talos_nmrPipe.tZ`.


### 2. Build NMRPipe in a docker container
```bash
$ ./nmrdock-build # this will take time to complete
```

### 3. Make the `nmrdock` command available
```bash
$ # for the current user only
$ ln -s ./nmrdock ~/.local/bin/nmrdock

$ # for all users (uncomment the command below)
$ # sudo ln -s ./nmrdock /usr/local/bin/nmrdock
```

## How to run

### Linux/Mac

```bash
$ # Navigate to the location of your data
$ cd /path/to/nmrdata/bruker/1
$ ls
pdata  audita.txt   format.temp   scon2       uxnmr.info
acqu   fid          fq1list       shimvalues  uxnmr.par
acqus  format.ased  pulseprogram  specpar     vtc_pid_setting

$ nmrdock

nmrdock@ab7383a3f7ba:~/data$ ls
pdata  audita.txt   format.temp   scon2       uxnmr.info
acqu   fid          fq1list       shimvalues  uxnmr.par
acqus  format.ased  pulseprogram  specpar     vtc_pid_setting

nmrdock@ab7383a3f7ba:~/data$ bruker # you can process the data using nmrpipe and write it out to this folder

nmrdock@ab7383a3f7ba:~/data$ ls # nmrpipe generates 4 new files fid.com, test.fid, nmr_ft.com, and test.ft1
pdata  audita.txt  format.ased  nmr_ft.com    shimvalues  test.ft1    vtc_pid_settings
acqu   fid         format.temp  pulseprogram  specpar     uxnmr.info
acqus  fid.com     fq1list      scon2         test.fid    uxnmr.par

nmrdock@ab7383a3f7ba:~/data$ exit

$ ls # these new files persist when you leave the container
pdata  audita.txt  format.ased  nmr_ft.com    shimvalues  test.ft1    vtc_pid_settings
acqu   fid         format.temp  pulseprogram  specpar     uxnmr.info
acqus  fid.com     fq1list      scon2         test.fid    uxnmr.par
```

### Windows

Following the instructions at https://compbiocore.github.io/nmrdock/walkthroughs/
