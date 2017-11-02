from parameters import *
import utility as ut
import index_data as idata
import esm

import struct
import os
import schema

input_dir = os.path.abspath("content/materials")
input_files = ut.get_file_list(input_dir)

materials = {}

for f in input_files:
    data = ut.read_newline_sep(f)
    material_type = (os.path.basename(f)).split('_')[1] # WEAP, ARMO, etc?
    materials[material_type] = {}
    for d in data:

        schemename = 'material_' + material_type
        mat = {}
        if (len(d) > 1):
            mat = schema.decode_plaintext(d[1:], schemename)
        if material_type == 'WEAP' and 'weapon_flags' not in mat:
            mat['weapon_flags'] = 0
        materials[material_type][d[0]] = mat

