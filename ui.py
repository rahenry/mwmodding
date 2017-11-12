import os
import ConfigParser
import StringIO
import subprocess
import time
from Tkinter import *
from MultiOrderedDict import MultiOrderedDict

root = Tk()

class gui:
    def __init__(self, master):
        self.master = master
        master.title = ("GUI")

        options_file = os.path.abspath('ui_options')
        self.options = ConfigParser.ConfigParser(dict_type = MultiOrderedDict)
        self.options.read(options_file)

        self.run_button = Button(root, command=self.run_main2, text='Run')
        self.run_button.grid(column=0, row=0)
        self.run_dummy = Button(root, text='Run', state=DISABLED)

        self.output_text = Text(root, height=10, width=30)
        self.output_text.grid(column=0, row=1)

        self.check_rebuild_icons = Checkbutton(root, text='Rebuild magic icons (requires ImageMagick)')
        self.check_rebuild_icons.grid(column=2, row=1)

    def run_main2(self):
        self.run_button['state'] = DISABLED
        self.run_button.grid_forget()
        self.run_button.update()
        self.run_dummy.grid(column=0, row=0)
        self.run_dummy.update()
        command = ['python', 'main.py']
        #subprocess.call(command)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        self.output_text.delete('1.0', END)
        self.output_text.insert(END, stdout)
        self.run_button['state'] = NORMAL
        self.run_button.update()
        self.run_button.grid(column=0, row=0)
        self.run_dummy.grid_forget()
        self.run_dummy.update()

gui1 = gui(root)
root.mainloop()

openmwcfg_path = '/home/rah/.config/openmw/openmw.cfg'
print openmwcfg_path
ini_str = '[root]\n' + open(openmwcfg_path, 'r').read()
ini_fp = StringIO.StringIO(ini_str)
openmwcfg = ConfigParser.ConfigParser(dict_type = MultiOrderedDict)
openmwcfg.readfp(ini_fp)
