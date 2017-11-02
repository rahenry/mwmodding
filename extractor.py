# functions for encoding and decoding ESM data

from parameters import *
import utility as ut
#import index_data as idata
import struct
import os

# extract all the mods in some folder, maybe with special rules, and build a openmw.cfg file to use them

MOD_DIRECTORY = '~/mwmodding/mods/'
archive_types = {
        'rar':{'command':'unrar x'},
        'zip':{'command':'unzip'},
        '7z':{'command':'7za x'},
        }

dl_path = os.path.abspath(os.path.expanduser(MOD_DIRECTORY) + '/downloads')
extract_path_base = os.path.abspath(os.path.expanduser(MOD_DIRECTORY) + '/extracted')
for f in ut.get_file_list(dl_path):
    for a, arc in archive_types.iteritems():
        if f.lower().endswith(a):

            extract_path = os.path.abspath(extract_path_base + '/' + os.path.basename(f))
            if not os.path.exists(extract_path):
                os.makedirs(extract_path)



def get_file_list(base_path):
    res = []
    for fname in os.listdir(base_path):
        path = os.path.join(base_path, fname)
        if os.path.isdir(path): continue
        res.append(path)
    return res

