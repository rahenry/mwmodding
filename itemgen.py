from parameters import *
import utility as ut
import index_data as idata
import esm

import struct
import os
import schema
import outputs
import item_types

input_dir = os.path.abspath("content/items")
input_files = {}
for d in ut.get_dir_list(input_dir):
    input_files[os.path.basename(d)] = ut.get_file_list(d)

new_items = {}

def read_id(s, rtype):
    return {'NAME' : s}

def read_enam(s, rtype):
    return {'ENAM' : PREFIX+s+NULL}

def read_copy(s, rtype):
    if s in esm.records_original[rtype]:
        return esm.records_original[rtype][s]

def read_type(s, rtype):
    s = s.split()
    res = {'material' : s[0],
            'type' : s[1],
            }
    type_id = (rtype, s[0], s[1])
    res.update(item_types.type_mappings[type_id])
    return res
            
read_map = {
        'id' : read_id,
        'enam' : read_enam,
        'type' : read_type,
        'copy' : read_copy,
        }

def read_item(d, rtype):
    res = {}
    res['FNAM'] = d[0]
    for x in d[1:]:
        x = x.split()
        ident = x[0]
        if ident in read_map:
            s = ' '.join(x[1:])
            #ut.update_non_existing_inplace(res, read_map[ident](s, rtype))
            res.update(read_map[ident](s, rtype))

    return res

for directory in input_files:
    rtype = os.path.basename(directory)
    new_items[rtype] = {}
    for f in input_files[rtype]:
        data = ut.read_newline_sep(f)
        for d in data:
            new_item = read_item(d, rtype)
            new_items[rtype][new_item['NAME']] = new_item



output_names = ['spellmod', 'everything']
outputs.update(new_items, output_names)

