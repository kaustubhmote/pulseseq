# base objects used by most cpython scripts



import tkinter as tk
from tkinter import Entry, Button

def getvals(*args):
    out = []
    for entry in args:
        out.append(entry)

def input(header='', info='',
        labels=[], values=[], types=[]):

    window = tk.Tcl()
    entries = [Entry(window) for _ in range(len(labels))]
    for entry in entries:
        entry.pack()

    btn=Button(window, text='OK', command=getvals(entries))
    
    return window.loadtk()    

if __name__ == "__main__":
    five = input(labels=['Yellow', 'Green'])
