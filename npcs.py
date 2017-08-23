from parameters import *
import utility as ut
import index_data as idata
import esm

import struct
import os
import schema
import outputs

test = 0
new_npcs = {}
last = ""
for name, npc in esm.records_original['NPC_'].iteritems():
    if 'player' not in name and 'orcerer' in npc['CNAM']:
        new_npcs[name] = dict(npc)
        schema.decode_all_subrecords(new_npcs[name])
        new_npcs[name]['strength'] = 100
        schema.encode_all_subrecords(new_npcs[name])


output_names = ['spellmod', 'everything']
outputs.update({'NPC_':new_npcs}, output_names)

