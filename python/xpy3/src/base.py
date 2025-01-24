"""
base.py: Base classes to be used in all cpython programs
This mainly consists of a detailed dialog box that can be
accessed to from the python

Author
------
Kaustubh R. Mote

Bugs/Suggestions
----------------
krmote@tifrh.res.in

"""

import os
from sys import argv
from tkinter import Tk, Entry, Label, Button, StringVar
from tkinter.ttk import Checkbutton, OptionMenu
import tkinter.font as tkFont


import tkinter as tk
from tkinter import font as tkFont
from tkinter import StringVar, Entry, Checkbutton, OptionMenu, Label, Button




def dialog(header="", info="", labels=[], types=[], values=[], comments=[]):
    """
    dialog box to specify parameters to run a script

    Parameters
    ----------
    header : str
        Header for the dialog box
    info : str
        Information about the program that will be run
    labels : list
        List of labels to use for each widget
    types : list
        Types of widgets allowed are Text-entry (e) Checkbox (c)
        and Drop-down menu (d)
    values : list
        List of default parameters to be put in each box
    comments : list
        Comments for each entry/checkbox/dropdown
    
    Returns
    -------
    entries : List
        A list of values put in by the user
    """

    # Set to blank values if none is given
    if values == []:
        values = [""] * len(labels)
    if comments == []:
        comments = [""] * len(labels)

    # Use Entry widget if no types are given
    if types == []:
        types = ["e"] * len(labels)

    # Check if lengths of each structure are the same
    for l in [types, values, comments]:
        if len(l) != len(labels):
            raise ValueError(
                """
            Number of elements in the list {0} 
            does not match the number of desired labeled widgets ({1})""".format(
                    l, len(labels)
                )
            )

    # Check that 'types' does not have anything other than 'e', 'c', or 'd'
    for i in types:
        if i.lower() not in ["e", "c", "d"]:
            raise ValueError("Input error. Type '{}' not understood".format(i))

    # Build the input window
    root = tk.Tk()
    root.title(header)
    nfont = tkFont.Font(family="Sans Serif", size=10)

    # Set padding for all widgets
    padding = {'padx': 10, 'pady': 5}

    # Information label
    Label(root, text=info, font=nfont, wraplength=300, justify="left", fg="blue").grid(
        sticky="w", row=0, column=0, columnspan=3, **padding
    )

    # Build labels and buttons
    entr, strvars = {}, {}
    for i, label in enumerate(labels):
        # Create widgets based on type
        if types[i] == "e":
            entr[i] = Entry(root, font=nfont)
        elif types[i] == "c":
            entr[i] = Checkbutton(root, text="", takefocus=False, font=nfont)
        elif types[i] == "d":
            strvars[i] = StringVar()
            entr[i] = OptionMenu(root, strvars[i], values[i][0], *values[i])
            entr[i].config(font=nfont)

        # Label for the input box
        Label(root, text=label, font=nfont).grid(sticky="w", row=i + 1, column=0, **padding)
        # Input widget
        entr[i].grid(sticky="w", row=i + 1, column=1, **padding)
        # Comment for the input box
        Label(root, text=comments[i], font=nfont, wraplength=200, justify="left").grid(
            sticky="w", row=i + 1, column=2, **padding
        )

        # Default values for text entry
        if types[i] == "e":
            entr[i].insert(0, values[i])
        # Default state for checkboxes
        elif types[i] == "c":
            if values[i]:
                entr[i].select()
            entr[i].grid(sticky="w", row=i + 1, column=1, columnspan=1, **padding)
        # Default value for dropdown
        elif types[i] == "d":
            strvars[i].set(values[i][0])

    # Get values if Submit is clicked
    def getvals():
        global entries
        entries = []
        for i in range(len(labels)):
            if types[i] == "e":
                entries.append(entr[i].get())
            elif types[i] == "c":
                entries.append(entr[i].var.get())
            elif types[i] == "d":
                entries.append(strvars[i].get())
        root.destroy()

    # Get no entries if Cancel is clicked
    def cancel():
        global entries
        entries = None
        root.destroy()

    # Submit/Cancel buttons
    Button(root, text="Submit", command=getvals, font=nfont).grid(row=len(labels) + 2, column=0, **padding)
    Button(root, text="Cancel", command=cancel, font=nfont).grid(row=len(labels) + 2, column=1, **padding)

    # Closing the window executes cancel
    root.protocol("WM_DELETE_WINDOW", cancel)

    # Place the window in approximately the center of the screen
    root.eval("tk::PlaceWindow %s center" % root.winfo_pathname(root.winfo_id()))

    # Run
    root.mainloop()
    return entries



















def dialog_old(header="", info="", labels=[], types=[], values=[], comments=[]):
    """
    dialog box to specify parameters to run a script

    Parameters
    ----------
    header : str
        Header for the dialog box
    info : str
        Information about the program that will be run
    labels : list
        List of labels to use for each widget
    types : list
        Types of widgets allowed are Text-entry (e) Checkbox (c)
        and Drop-down menu (d)
    values : list
        List of default parameters to be put in each box
    comments : list
        Comments for each entry/checkbox/dropdown
    
    Returns
    -------
    entries : List
        A list of values put in by the user
    
    """

    # set to blank values if none is given
    if values == []:
        values = [""] * len(labels)
    if comments == []:
        comments = [""] * len(labels)

    # Use Entry widget if no types are given:
    if types == []:
        types = ["e"] * len(labels)

    # check if lengths of each structure are same
    for l in [types, values, comments]:
        if len(l) != len(labels):
            raise ValueError(
                """
            Number of elements in the list {0} 
            does not match the number of desired labeled widgets ({1})""".format(
                    l, len(labels)
                )
            )

    # check that 'types' does not have anything other than 'e' or 'c'
    for i in types:
        if i.lower() not in ["e", "c", "d"]:
            raise ValueError("Input error. Type '{}' not understood".format(i))

    # build the input window
    root = Tk()
    nfont = tkFont.Font(family="lucidabright", size=20, weight=tkFont.NORMAL)
    root.option_add("*Font", nfont)
    root.title(header)

    Label(
        root, text=info, font=nfont, wraplength=300, justify="left", fg="blue",
    ).grid(sticky="w", row=0, column=0, columnspan=9, pady=(5, 20), padx=(5, 5))

    # build labels and buttons
    entr, strvars = {}, {}
    for i, label in enumerate(labels):
        # TEXT ENTRY
        if types[i] == "e":
            entr[i] = Entry(root)
        # CHECKBOX
        elif types[i] == "c":
            entr[i] = Checkbutton(root, text="", takefocus=False)
        # DROPDOWN MENU
        elif types[i] == "d":
            strvars[i] = StringVar()
            entr[i] = OptionMenu(root, strvars[i], values[i][0], *values[i])

        # Label for the input box
        Label(root, text=label, font=nfont).grid(
            sticky="w", row=i + 1, column=0, padx=(5, 5)
        )
        # Comment for the input box
        Label(root, text=comments[i], font=nfont, wraplength=100, justify="left").grid(
            sticky="w", row=i + 1, column=8, columnspan=1, padx=(5, 5), pady=(5, 5)
        )

        # TEXT ENTRY
        if types[i] == "e":
            entr[i].grid(
                sticky="w", row=i + 1, column=1, columnspan=7, pady=(5, 5), padx=(5, 5)
            )
            entr[i].insert(0, values[i])
        # CHECKBOX
        if types[i] == "c":
            entr[i].grid(
                sticky="w", row=i + 1, column=1, columnspan=1, pady=(5, 5), padx=(5, 5)
            )
            entr[i].state(["!alternate"])
        # Dropdown Menu
        if types[i] == "d":
            entr[i].grid(
                sticky="w", row=i + 1, column=1, columnspan=3, pady=(5, 5), padx=(5, 5)
            )

    # get values if Submit is clicked
    def getvals():
        global entries
        entries = []
        for i in range(len(labels)):
            if types[i] in ["e"]:
                entries.append(entr[i].get())
            elif types[i] == "c":
                entries.append(entr[i].state())
            elif types[i] in ["d"]:
                entries.append(strvars[i].get())
        root.destroy()

    # get no entries if cancel is clicked
    def cancel():
        global entries
        entries = None
        root.destroy()

    # Submit/Cencel buttons
    Button(root, text="Submit", command=getvals).grid(row=len(labels) + 2, column=0)
    Button(root, text="Cancel", command=cancel).grid(row=len(labels) + 2, column=1)

    # Closing the window executes cancel
    root.protocol("WM_DELETE_WINDOW", cancel)

    # Place the window in approximately the center of the screen
    root.eval("tk::PlaceWindow %s center" % root.winfo_pathname(root.winfo_id()))

    # Run
    root.mainloop()
    return entries


def text_entry():
    """ Single Multiline Entry Textbox"""

    from tkinter import Text, Tk, Button

    root = Tk()
    root.title("Enter the recombination matrix")
    root.geometry("600x400")
    mat = Text(root, height=25, width=80)
    mat.pack()

    # get values if Submit is clicked
    def getvals():
        global entries
        entries = mat.get("1.0", "end-1c")
        root.destroy()

    # get no entries if cancel is clicked
    def cancel():
        global entries
        entries = None
        root.destroy()

    # Submit/Cencel buttons
    submit = Button(root, text="Submit", command=getvals)
    cancel = Button(root, text="Cancel", command=cancel)
    submit.pack()
    cancel.pack()

    # Closing the window executes cancel
    root.protocol("WM_DELETE_WINDOW", cancel)

    # Place the window in approximately the center of the screen
    root.eval("tk::PlaceWindow %s center" % root.winfo_pathname(root.winfo_id()))

    # Run
    root.mainloop()
    return entries
