import tkinter
from tkinter import filedialog

idir = 'C:\\python_test'
file_path = tkinter.filedialog.askopenfilename(initialdir = idir)

print(file_path)