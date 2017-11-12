import os
import ConfigParser
import StringIO
import subprocess
import time
from Tkinter import *
from MultiOrderedDict import MultiOrderedDict
import utility as ut
import tkFileDialog

def run_main2():
    run_button['state'] = DISABLED
    run_button.grid_forget()
    run_button.update()
    run_dummy.grid(column=0, row=0)
    run_dummy.update()
    command = ['python', 'main.py']
    #subprocess.call(command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    output_text.delete('1.0', END)
    output_text.insert(END, stdout)
    run_button['state'] = NORMAL
    run_button.update()
    run_button.grid(column=0, row=0)
    run_dummy.grid_forget()
    run_dummy.update()

def choose_path(entry):
    #s = tkFileDialog.askopenfilename()
    s = '123'
    print s

root = Tk()

options_file = os.path.abspath('ui_options')
options = ConfigParser.ConfigParser(dict_type = MultiOrderedDict)
options.read(options_file)

run_button = Button(root, command=run_main2, text='Run')
run_button.grid(column=0, row=0)
run_dummy = Button(root, text='Run', state=DISABLED)

path_entry = Entry(root)
path_entry.grid(column=0, row=1)
path_entry_button = Button(root, text='Select', command=lambda: choose_path(path_entry))
path_entry_button.grid(column=1, row=1)

output_text = Text(root, height=10, width=30)
output_text.grid(column=0, row=2)

if False:
    check_rebuild_icons = Checkbutton(root, text='Rebuild magic icons (requires ImageMagick)')
    check_rebuild_icons.grid(column=2, row=1)

root.mainloop()

openmwcfg_path = os.path.abspath(os.path.expanduser('~/.config/openmw/openmw.cfg'))
print ut.read_headless_config(openmwcfg_path)
