from parameters import *
import utility as ut
import index_data as idata
import esm

import struct
import os
import schema
import outputs
import spellgen

input_dir = os.path.abspath("content/enchantments")
input_files = ut.get_file_list(input_dir)

def read_ench(d):
    res = {}
    res['NAME'] = PREFIX + 'en_' + d[0]
    res.update(schema.decode_plaintext(d[1].split(), 'ENDT'))
    res['ENDT'] = {}
    schema.record_repack_schema(res)
    res['ENAM'] = []
    for x in d[2:]:
        res['ENAM'].append(spellgen.build_ENAM(x, None, False)['data'])
    return res
    


new_enchs= {}
for f in input_files:
    data = ut.read_newline_sep(f)
    for d in data:
        new_ench = read_ench(d)
        new_enchs[new_ench['NAME']] = new_ench



output_names = ['spellmod', 'everything']
outputs.update({'ENCH' : new_enchs}, output_names)

