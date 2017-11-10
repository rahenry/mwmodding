import argparse
import configparser
from collections import OrderedDict

ini_str = '[root]\n' + open(ini_path, 'r').read()
ini_fp = StringIO.StringIO(ini_str)
config = ConfigParser.RawConfigParser()
config.readfp(ini_fp)

class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(MultiOrderedDict, self).__setitem__(key, value)
            # super().__setitem__(key, value) in Python 3

parser = argparse.ArgumentParser()
parser.add_argument('--input_file', nargs=1, default='defaults')
#parser.add_argument('--regenerate_spell_icons', nargs=1, default=True, type=bool)
#parser.add_argument('--npcs', nargs=1, default=True, type=bool)
args = parser.parse_args()

print args.input_file

options = configparser.ConfigParser(dict_type = MultiOrderedDict)
options.read(args.input_file)


openmwcfg = configparser.ConfigParser(dict_type = MultiOrderedDict)
openmwcfg.read('/home/rah/.config/openmw/openmw.cfg')



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

