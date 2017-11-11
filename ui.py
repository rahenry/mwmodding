import os
import ConfigParser
import StringIO
import subprocess
from Tkinter import *
from MultiOrderedDict import MultiOrderedDict

class gui:
    def __init__(self, master):
        self.master = master
        master.title = ("GUI")

        options_file = os.path.abspath('ui_options')
        self.options = ConfigParser.ConfigParser(dict_type = MultiOrderedDict)
        self.options.read(options_file)

        self.run_button = Button(root, command=self.run_main, text='Run')
        self.run_button.grid(column=0, row=0)

    def run_main(self):
        command = ['python', 'main.py']
        self.proc = subprocess.Popen(command)

        self.master.state('disabled')
        while self.proc.poll() is None:
            1

root = Tk()
gui1 = gui(root)
root.mainloop()

openmwcfg_path = '/home/rah2/.config/openmw/openmw.cfg'
ini_str = '[root]\n' + open(openmwcfg_path, 'r').read()
ini_fp = StringIO.StringIO(ini_str)
openmwcfg = ConfigParser.ConfigParser(dict_type = MultiOrderedDict)
openmwcfg.readfp(ini_fp)
