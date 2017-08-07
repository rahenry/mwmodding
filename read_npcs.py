import random
import subprocess
import os
import re
import struct

mw_data_dir = "~/.local/share/openmw/data"
mw_data_files = ["Morrowind.esm", "Tribunal.esm", "Bloodmoon.esm"]

for d in mw_data_files:
    path = mw_data_dir + "/" + d
    f = open(path)

