'''
xcpy.py
(To be executed using Jython from within Topspin)

Contains the locations of the following items: 
    - (C)Python that will execute scripts
    - Will pass the current EXPNO, PROCNO and Folder to the 
      script that is being executed

Bugs/Suggestions
----------------
kaustuberm@tifrh.res.in
'''

import sys, os 
from subprocess import Popen, PIPE, STDOUT

def cpython(cpyname='/home/kaustubh/miniconda/envs/nmr-py37/bin/python', args=sys.argv):
    """
    Sets the path for the executable for Cpython to be used

    Parameters
    ----------
    cpyscript : str
        path to the cpython executable

    Returns
    -------
    cpyscript : str
        path to the executable.
        Checks whether the xcpy.py script was invoked with the -p or --python
        argumetnt and if yes, pops open a dialog box to ask/show the cpython
        that is being used

    Notes
    -----
    LINUX
    Change this default assignment of cpyname to the python you want to use. 
    Eg '/usr/bin/python3' or a specific environment (as is the default)
    Use full filepaths, Eg  (1) use '/usr/bin/python', not 'python' 
                            (2) use '/home/env/python' not '~/env/python'
                            (3) use '/home/env/python' not '$HOME/env/python' 

    MACINTOSH
    Untested

    WINDOWS
    Change this default assignment of cpyname to the python you want to use. 
    C:\<PATH-TO-PYTHON>\python.exe (needs to be specified with the .exe extension)
    
    
    """
    # check if script is invoked with '-p or --python argumet'
    # this opens up a dialog box to take in python to use
    if len(args) >= 3:
        if args[2] in ['-p', '--python']:
            cpyname = INPUT_DIALOG(title='PYTHON EXECUTABLE',
                                   header="""
                                   Specify python executable to use. 
                                   See the guide in docstring for the set_cpython 
                                   function in 'xcpy.py' for more information on how 
                                   to specify this paths.
                                   """,
                    items=['CPython Executable'],
                    values=[cpyname],
                    types=[''],
                    comments=[''])
        return str(cpyname[0])
    else:
        return cpyname

# set the python executable
cpy_executable = cpython()

# Folder of the TOPSPIN directory
try:
    # TopSpin >= 3.6
    toppath = sys.getBaseProperties()['XWINNMRHOME']
except:
    try:
        # TOPSPIN > 3.1 and < 3.5
        toppath = sys.registry['XWINNMRHOME'] 
    except:
        # TOPSPIN < 3.1
        toppath = sys.getEnviron()['XWINNMRHOME'] 

# Folder for the cpython scripts
cpyfolder = os.path.join(toppath, 'exp', 'stan', 'nmr', 'py', 'user', 'cpython')

# Get current data folders
try:
    cd = CURDATA()
    curdir = os.path.join(cd[3], cd[0])
    curexpno = cd[1]
    curprocno = cd[2]
except:
    raise ValueError('No datafolder detected. You have to join an experient to execute this command.')

# get scriptname
cpyscript = sys.argv[1]
# check if file exists, and try with a .py extension as well
scriptname = os.path.join(cpyfolder, cpyscript) 
if not os.path.isfile(scriptname):
    scriptname = os.path.join(cpyfolder, cpyscript+'.py')
    if not os.path.isfile(scriptname):
        raise NameError('The cpython script {} does not exist in the {} folder'.format(cpyscript, cpyfolder))

# Use shell if the OS is Windows. Needs to be tested on multiple OSs
if os.name == 'nt':
    use_shell = True
else:
    use_shell = False

# RUN the cpython script giving it information on the current dataset
p = Popen([cpy_executable, scriptname, curdir, curexpno, curprocno], 
           stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=use_shell)
p.stdin.close()

# Read in any stdout messege if the cpython script fails 
errmsg = []	
for line in iter(p.stdout.readline, ''):
   errmsg.append(line)
         
# Display the error message
if not errmsg:
    MSG('Script executed to completion.')
else:
    MSG(''.join(errmsg))
