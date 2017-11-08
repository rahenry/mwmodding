# find mod files by looking in various paths, etc.

from parameters import *
import utility as ut
import index_data as idata
import struct
import os

data_files = []
for f in ut.get_file_list(MW_DATA_PATH):
    if not 'orrow' in f: continue
    if '.esm' in f: data_files.append(os.path.abspath(f))
#data_files = ["test.esm"]

