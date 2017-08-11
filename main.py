import struct 
import index_data
import mwdata
record_types_of_interest = ['MGEF', 'SPEL', 'SCPT', 'RACE']
records = mwdata.extract_records(record_types_of_interest)

import magic_effects
magic_effects.process_mgefs(records)
import spellgen
import buffs
import races


test_output = {'SPEL' : spellgen.spells,
        'SCPT' : buffs.scripts,
        }
f = open("new_spells.esp", 'w+')
f.write(mwdata.write_esp(test_output))

#for i in range(100):
    #print (i, spellgen.convert_skill_to_cost(i))

#for ind, race in records['RACE'].iteritems():
    #print ind
