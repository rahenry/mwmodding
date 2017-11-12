import argparse
import ConfigParser
import StringIO
from MultiOrderedDict import MultiOrderedDict


parser = argparse.ArgumentParser()
parser.add_argument('--input_file', nargs=1, default='defaults')
#parser.add_argument('--regenerate_spell_icons', nargs=1, default=True, type=bool)
#parser.add_argument('--npcs', nargs=1, default=True, type=bool)
args = parser.parse_args()

print args.input_file

options = ConfigParser.ConfigParser(dict_type = MultiOrderedDict)
options.read(args.input_file)


openmwcfg_path = '/home/rah/.config/openmw/openmw.cfg'
ini_str = '[root]\n' + open(openmwcfg_path, 'r').read()
ini_fp = StringIO.StringIO(ini_str)
openmwcfg = ConfigParser.ConfigParser(dict_type = MultiOrderedDict)
openmwcfg.readfp(ini_fp)




import index_data
import esm
import schema
import outputs
import magic_effects
magic_effects.process_mgefs(options)
import spellgen
import materials
import item_types
import races
import npcs
npcs.process_npcs(options)
import scripts
import enchantments
import itemgen
import spells
outputs.write()

