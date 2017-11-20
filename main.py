import sys
import config
import index_data
import esm
esm.extract_records(config.mod_paths)
import schema
import outputs
import magic_effects
magic_effects.process_mgefs()
import spellgen
import materials
import item_types
import races
import npcs
npcs.process_npcs()
import scripts
import enchantments
import itemgen
import spells
outputs.write()

