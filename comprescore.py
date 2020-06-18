#!/usr/bin/env python
# Weissman Imports
from __future__ import division
import os
import sys
import time
import gzip
import tempfile
import subprocess
from math import log
import argparse

# GUI Imports
import tkinter
import tkinter as tk
import tkinter as ttk
from tkinter import Menu
import subprocess
import os
from tkinter import Menu
from tkinter import filedialog
from tkinter import messagebox as msg
import tkinter.ttk as TTK

# Imports

# Global Variables
__version__ = 0.1

# FONT SIZE
FONT_SIZE = 20

# COLORS
COLOR_WHITE = "#FFFFFF"
COLOR_RED = "#ff2a2a"
COLOR_BLUE = "#4645df"

# FONT STYLES
FONT_STYLE = ('Helvetica', FONT_SIZE, 'bold')
FONT_STYLE_1 = ('monospace', FONT_SIZE, 'bold')


main_win = tk.Tk()
main_win.title("Comprescore .v1")

# Functions

# About
def about():
    about_win = tk.Tk()
    about_win.title("Comprescore .v1 - About")

    about_main_frame = tkinter.LabelFrame(about_win, text="About")
    about_main_frame.grid(column=0, row=0, padx=5, pady=5)

    about_label = tkinter.Label(about_main_frame, bg=COLOR_WHITE, font=FONT_STYLE, text="Comprescore .v1")
    about_label.grid(column=0, row=0, padx=0, pady=0)

    about_text_label = tkinter.Label(about_main_frame, text="Comprescore .v1 - Compression Algorithm Effciency Checking Tool \n\n compare the effciency score of compression algorithms. \n 'Higher the score, better the alogrithm.' \n\n   Compiled on: 08-06-2020\n Developed by Hyper-Programmer ")
    about_text_label.grid(column=0, row=1, padx=0, pady=0)

    about_win.resizable(False, False)
    about_win.mainloop


# Select file to compress
def select_file():
    global filename
    filename = filedialog.askopenfilename(initialdir="/", title="Select file")
    filename_label.configure(text=filename)

# Exit (Quit)
def quit():
    main_win.quit
    main_win.destroy
    exit()


# Read Inputs
def read_data():
    if filename == "":
        msg.showerror(title="File not Selected", message="Select File for Compression.")

    else:
        # command_value = command_combobox.get()+' '+filename
        alpha_value = int(alpha_spinbox.get())
        repetition_value = int(repetition_spinbox.get())
        uncommpressed_selected_file = filename


        if command_combobox.get() == "bzip2 (ext/.bzip2)":
            command_value = "bzip2 --keep"+' '+filename
            commpressed_selected_file = filename+".bz2"
            # Weissman's Code
            W = weissman(command_value, uncommpressed_selected_file, commpressed_selected_file, alpha_value, repetition_value)
            # print('Weissman score: %s' % str(W))
            # Weissman's Code

            # console_log = subprocess.run(['python', 'weissman.py', '-c', command_value, '-i', uncommpressed_selected_file, '-o', commpressed_selected_file, '-a', alpha_value, '-r', repetition_value], stdout=subprocess.PIPE)

            # console_log = os.system(command_value)
            display_score.configure(text=str(W))

        elif command_combobox.get() == "gzip (ext/.gz)":
            command_value = "gzip --keep"+' '+filename
            commpressed_selected_file = filename+".gz"
            W = weissman(command_value, uncommpressed_selected_file, commpressed_selected_file, alpha_value, repetition_value)
            display_score.configure(text=str(W))

# Weissman Algorithm's Code
def gzip_compr_test(fname, compresslevel=9):
    """Return compression ratio and time-to-compress using gzip
    
    Parameters
    ----------
    fname : string
        The path to the file to compress
    compresslevel : int, optional
        The compression level used
    
    Returns
    -------
    r : float
        The compression ratio
    T : float
        The time-to-compress
    """
    fname_compr = tempfile.mkstemp(suffix='.gz')[1]
    with open(fname, 'rb') as f_in:
        with gzip.open(fname_compr, 'wb', compresslevel=compresslevel) as f_out:
            t_start = time.time()
            f_out.writelines(f_in)
            T = time.time() - t_start
    r = os.path.getsize(fname)/os.path.getsize(fname_compr)
    os.remove(fname_compr)
    return r, T

def target_compr_test(command, fname_in, fname_out):
    """Return compression ratio and time-to-compress using a given compression 
    algorithm
    
    Parameters
    ----------
    command : string
        The command for executing the compression algorithm
    fname_in : string
        The path to the uncompressed file which will be compressed by the command
    fname_out : string
        The path to the compressed file generated by the command
    
    Returns
    -------
    r : float
        The compression ratio
    T : float
        The time-to-compress
    """
    t_start = time.time()
    retcode = subprocess.call(command.split(" "))
    T = time.time() - t_start
    r = os.path.getsize(fname_in)/os.path.getsize(fname_out)
    if retcode != 0:
        raise ValueError("The target algorithm returned with code %d, something went wrong"
                         % retcode)
    os.remove(fname_out)
    return r, T

def weissman(command, fname_in, fname_out, alpha, reps):
    """Compute the Weissman score of a compression algorithm using Gzip as
    baseline.
    
    Parameters
    ----------
    command : string
        The command for executing the compression algorithm
    fname_in : string
        The path to the uncompressed file which will be compressed by the command
    fname_out : string
        The path to the compressed file generated by the command
    alpha : float
        The scaling factor
    reps : int
        The number of times compression test is repeated
        
    Returns
    -------
    W : float
        The Weissman score
    """
    mean = lambda x: sum(x)/len(x)
    r, T = [mean(x)
            for x in zip(*[target_compr_test(command, fname_in, fname_out)
                           for _ in range(reps)])]
    r_b, T_b = [mean(x)
                for x in zip(*[gzip_compr_test(fname_in)
                               for _ in range(reps)])]
    return alpha * (r/r_b) * (log(T_b)/log(T))
# Weissman Algorithm's Code

# GUI Constructions


def Main():

    # ####################### FRAMES ############################

    # Display Frame
    display_score_frame = tkinter.LabelFrame(main_win,text="Compress Efficency Score")
    display_score_frame.grid(column=0, row=0,  padx=5, pady=5)

    # Button Frame
    button_frame = tkinter.LabelFrame(main_win, text="Calculate")
    button_frame.grid(column=0, row=10,  padx=5, pady=5)

    # Main_Frame
    inputs_frame = tkinter.LabelFrame(main_win,text="Inputs")
    inputs_frame.grid(column=0, row=1,  padx=5, pady=5)

    # Inputs - Main Frame 3
    inputs_frame_1 = tkinter.Frame(inputs_frame)
    inputs_frame_1.grid(column=0, row=0,  padx=5, pady=5)

    # Inputs - Main Frame 4
    inputs_frame_2 = tkinter.Frame(inputs_frame)
    inputs_frame_2.grid(column=0, row=1,  padx=5, pady=5)

    # Command Entry Frame
    command_combobox_frame = tkinter.LabelFrame(inputs_frame_1, text="Command (Compression Algorithm) ")
    command_combobox_frame.grid(column=0, row=1,  padx=5, pady=5, sticky="w")

    # File input Frame
    file_input_frame = tkinter.LabelFrame(inputs_frame_1, text="Select File to Compress ")
    file_input_frame.grid(column=0, row=0,  padx=5, pady=5, sticky="w")

    # Alpha Constant Entry Frame
    alpha_spinbox_frame = tkinter.LabelFrame(inputs_frame_2, text="Alpha Scaling Constant")
    alpha_spinbox_frame.grid(column=0, row=1,  padx=5, pady=5, sticky="w")

    # Repetition Entry Frame
    repetition_spinbox_frame = tkinter.LabelFrame(inputs_frame_2, text="Repetition Constant")
    repetition_spinbox_frame.grid(column=1, row=1,  padx=5, pady=5, sticky="w")

    # Menu Bar

    menu_bar = Menu(main_win)
    main_win.config(menu = menu_bar)

    # Menu Items

    menu_file = Menu(menu_bar, tearoff=0)
    menu_file.add_command(label="Exit", command=quit)
    menu_bar.add_cascade(label="File", menu=menu_file)

    menu_about = Menu(menu_bar, tearoff=0)
    menu_about.add_command(label="About", command=about)
    menu_bar.add_cascade(label="Help", menu=menu_about)

    # Tabs

    # tab_control = ttk.NO(main_win)
    # tab1 = ttk.Frame(main_win)
    # tab_control.add(tab1, text='Main')
    # tab_control.pack(expand=1, fill="both")



    # ####################### WIDGETS ############################

    # Display Score
    global display_score
    display_score = tkinter.Label(display_score_frame, bg=COLOR_WHITE, font=FONT_STYLE_1, text="", width=35, height=2)
    display_score.grid(column=0, row=1, padx=5, pady=5)


    # Command Inputs
    global command_combobox
    # command_combobox = tkinter.Entry(command_combobox_frame,bg=COLOR_WHITE, width=35)
    # command_combobox.grid(column=0, row=3, padx=5, pady=5)
    command_combobox = TTK.Combobox(command_combobox_frame, width=70)
    command_combobox.grid(column=0, row=3, padx=5, pady=5)
    command_combobox['values'] = ("bzip2 (ext/.bzip2)", "gzip (ext/.gz)")
    command_combobox.current(0)


    # Show Selected Filename
    global filename_label
    filename_label = tkinter.Label(file_input_frame, text="Select file..", width=50)
    filename_label.grid(column=0, row=0, padx=5, pady=5)


    # File Select Dialog
    global select_filedialog, filename
    filename = ""
    select_filedialog = tkinter.Button(file_input_frame, text="Browse File..", command=select_file)
    select_filedialog.grid(column=1, row=0, padx=5, pady=5)

    # ALpha Costant Read input
    global alpha_spinbox
    alpha_spinbox = tkinter.Spinbox(alpha_spinbox_frame, width=35, from_=1, to=10)
    alpha_spinbox.grid(column=0, row=5, padx=5, pady=5)

    # Repetition Read input
    global repetition_spinbox
    repetition_spinbox = tkinter.Spinbox(repetition_spinbox_frame, width=35, from_=1, to=100)
    repetition_spinbox.grid(column=1, row=5, padx=5, pady=5)

    # Combo Box
    # algo_combo = tkinter.Combobox

    # Calculate Button
    calc_btn = tkinter.Button(button_frame,bg=COLOR_RED, text="Calculate", width=65, height=2, command = read_data)
    calc_btn.grid(column=0, row=0, padx=5, pady=5)

    # Icon for Main Window
    # main_win.iconbitmap('comprescore.ico')

    # Loop
    main_win.resizable(False, False)
    main_win.mainloop()

if __name__ == "__main__":
    Main()