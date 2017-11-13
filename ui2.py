import os
import ConfigParser
import StringIO
import subprocess
import time
from Tkinter import *
from MultiOrderedDict import MultiOrderedDict
import utility as ut
import tkFileDialog

mwini_path = ''
def run_main2():
    run_button['state'] = DISABLED
    run_button.grid_forget()
    run_button.update()
    run_dummy.grid(column=0, row=1)
    run_dummy.update()
    command = ['python', 'main.py']
    #subprocess.call(command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    output_text.delete('1.0', END)
    output_text.insert(END, stdout)
    run_button['state'] = NORMAL
    run_button.update()
    run_button.grid(column=0, row=1)
    run_dummy.grid_forget()
    run_dummy.update()

def choose_path(text_widget):
    s = tkFileDialog.askopenfilename()
    text_widget['state'] = NORMAL
    text_widget.update()
    text_widget.delete(0, END)
    text_widget.insert(0, s)
    text_widget.xview_moveto(1)
    text_widget['state'] = 'readonly'
    mwini_path = s

def choose_save_file(text_widget):
    s = tkFileDialog.asksaveasfilename()
    text_widget['state'] = NORMAL
    text_widget.update()
    text_widget.delete(0, END)
    text_widget.insert(0, s)
    text_widget.xview_moveto(1)
    text_widget['state'] = 'readonly'
    mwini_path = s

def on_closing():
    save_options()
    root.destroy()

def save_options():
    options.set('settings', 'inputpath', inputpath_text.get())
    options.set('settings', 'outputpath', outputpath_text.get())
    options.write(open('ui_options', 'w+'))

def read_options():
    options.get('settings', 'inputpath')
    if options.has_option('settings', 'inputpath'):
        inputpath_text.delete(0, END)
        inputpath_text.insert(END, options.get('settings', 'inputpath'))
    if options.has_option('settings', 'outputpath'):
        outputpath_text.delete(0, END)
        outputpath_text.insert(END, options.get('settings', 'outputpath'))


options = ConfigParser.ConfigParser(dict_type = MultiOrderedDict)
options_file = os.path.abspath('ui_options')
options.read(options_file)

root = Tk()


run_button = Button(root, command=run_main2, text='Run')
run_button.grid(column=0, row=3)
run_dummy = Button(root, text='Run', state=DISABLED)
output_text = Text(root, height=10)
output_text.grid(column=0, row=4, columnspan=3)

#inputpath_text = Text(root, width=25, height=1)
inputpath_label = Label(root, text='Path to morrowind.ini or openmw.cfg:', anchor=E)
inputpath_label.grid(column=0, row=1, sticky=E)
inputpath_text = Entry(root)
inputpath_text.grid(column=1, row=1)
inputpath_text_button = Button(root, text='Select', command=lambda: choose_path(inputpath_text))
inputpath_text_button.grid(column=2, row=1)

outputpath_label = Label(root, text='Output path:', anchor=E)
outputpath_label.grid(column=0, row=2, sticky=E)
outputpath_text = Entry(root)
outputpath_text.grid(column=1, row=2)
outputpath_text_button = Button(root, text='Select', command=lambda: choose_save_file(outputpath_text))
outputpath_text_button.grid(column=2, row=2)

read_options()
outputpath_text['state'] = 'readonly'
inputpath_text['state'] = 'readonly'

title_label = Label(root, text='Sweet Config Program', font=("Helvetica", 24))
title_label.grid(column=0, row=0, columnspan=3)
if False:
    check_rebuild_icons = Checkbutton(root, text='Rebuild magic icons (requires ImageMagick)')
    check_rebuild_icons.grid(column=2, row=1)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
#save_options()

openmwcfg_path = os.path.abspath(os.path.expanduser('~/.config/openmw/openmw.cfg'))
#print ut.read_headless_config(openmwcfg_path)
