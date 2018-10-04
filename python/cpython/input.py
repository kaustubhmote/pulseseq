'''
phase_shift: adds an arbitrary phase shift to the raw FID/SER file
and writes it to a new directory

Usage
-----
User will be prompted for the experiment number to output the file to 
and the phase shift in degrees

Author
------
Kaustubh R. Mote

Bugs/Suggestions
----------------
kaustuberm@tifrh.res.in

'''

import os
from sys import argv

from tkinter import simpledialog, Entry, Tk, Label


class MyDialog(simpledialog.Dialog):

    def body(self, master):

        Label(master, text="First:").grid(row=0)
        Label(master, text="Second:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        first = self.e1.get()
        second = self.e2.get()
        print(first, second)

root = Tk() 
d = MyDialog(root)
print(d.result)
