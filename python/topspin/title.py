"""
title.py

"""
import sys, os, datetime

argv = sys.argv
curexpname, curexpno, curprocno, curdir = CURDATA()


if argv[1] not in ["-a", "-p", "-c"]:
    newargs = []
    newargs.append(argv[0])
    newargs.append("-a")
    for i in argv[1:]:
        newargs.append(i)
    argv = newargs
title_path = os.path.join(curdir, curexpname, curexpno, "pdata", curprocno, "title")


with open(title_path, "r") as f:
    title = f.read()


if argv[2] == "date":
    title_new = datetime.date.today().strftime("%d %B %Y")
else:
    title_new = " ".join(argv[2:])


with open(title_path, "r") as f:
    title = f.read()

    if argv[1] == "-p":
        title_new = title_new + "\n" + title

    elif argv[1] == "-a":
        title_new = title + "\n" + title_new

    elif arg[1] == "-o":
        pass

    elif argv[1] == "-c":
        copy_title_path = os.path.join(
            curdir, curexpname, argv[2], "pdata", "1", "title"
        )
        with open(copy_title_path, "r") as fcopy:
            title_new = fcopy.read()

with open(title_path, "w") as f:
    f.write(title_new)
