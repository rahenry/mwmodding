import struct 
import index_data
import mwdata
record_types_of_interest = ['MGEF', 'SPEL', 'SCPT', 'RACE', 'NPC_']
records = mwdata.extract_records(record_types_of_interest)

import magic_effects
magic_effects.process_mgefs(records)
import spellgen
import buffs
import races
races.process_races(records)

import npcs
spellmaking_npcs = npcs.populate_npcs(records, spellgen.spells)

test_output = {'SPEL' : spellgen.spells,
        'SCPT' : buffs.scripts,
        #'RACE' : races.races,
        'NPC_' : spellmaking_npcs,
        }
f = open("test.esp", 'w+')
f.write(mwdata.write_esp(test_output))

#for i in range(100):
    #print (i, spellgen.convert_skill_to_cost(i))

#for ind, race in records['RACE'].iteritems():

    #print ind
