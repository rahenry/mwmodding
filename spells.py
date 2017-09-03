from parameters import *
import utility as ut
import index_data as idata
import esm
import random

import struct
import os
import schema
import outputs
import spellgen

# remove autocalc and pcstart from all existing spells
reflagged_spells = {}
for name, spell in esm.records_original['SPEL'].iteritems():
    spell.update(schema.decode_subrecord(spell['SPDT'], 'SPDT'))
    spellflags = bin(spell['spell_flags'])[2:].zfill(4)
    if spellflags[-1] == '1' or spellflags[-2] == '1':
        new_spell = dict(spell)
        if spellflags[-3] == '1': 
            new_spell['spell_flags'] = int('0100', 2)
        else:
            new_spell['spell_flags'] = int('0000', 2)
        new_spell['SPDT'] = schema.encode_subrecord(new_spell, 'SPDT')
        reflagged_spells[name] = new_spell

for name, spell in reflagged_spells.iteritems():
    1

output_names = ['spellmod', 'everything']
outputs.update({'SPEL':reflagged_spells}, output_names)
