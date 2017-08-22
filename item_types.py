from parameters import *
import utility as ut
import index_data as idata
import esm

import struct
import os
import schema
import utility as ut

input_dir = os.path.abspath("content/item_types")
input_files = ut.get_file_list(input_dir)
item_types = {}

for f in input_files:
    data = ut.read_newline_sep(f)
    rec_type = (os.path.basename(f)).split('_')[0]
    item_types[rec_type] = {}
    for d in data:
        schemename = rec_type + '_type'
        t = {}
        name = ut.reductions(d[0])
        if rec_type == 'WEAP': d = d[1:]

        if (len(d) > 1):
            t = schema.decode_plaintext(d, schemename)
        item_types[rec_type][name] = t

