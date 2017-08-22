import index_data
import esm
import schema
import magic_effects
import spellgen
import materials
import item_types
import scripts



res = {}
res.update({'SPEL' : spellgen.new_spells})

esm.write_esp(res, 'test.esp')
