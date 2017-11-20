import argparse
import ConfigParser
import StringIO
from MultiOrderedDict import MultiOrderedDict
import os
import utility as ut

CONFIG_DEFAULTS = {
        'regenerate_spell_icons' : '0',
        'process_npcs' : '1',
        'output_path' : 'output.esp',
        'modlist_path': '~/.config/openmw/openmw.cfg',
        'options_path' : 'ui_options',
        }

parser = argparse.ArgumentParser()
parser.add_argument('--input_file', nargs=1, default=[''])
#parser.add_argument('--output_file', nargs=1, default='output.esp')
#parser.add_argument('--regenerate_spell_icons', nargs=1, default=True, type=bool)
#parser.add_argument('--npcs', nargs=1, default=True, type=bool)
args = parser.parse_args()

def add_missing_header(path):
    ini_str = '[settings]\n' + open(path, 'r').read()
    ini_fp = StringIO.StringIO(ini_str)
    res = ConfigParser.ConfigParser(CONFIG_DEFAULTS, dict_type = MultiOrderedDict)
    res.readfp(ini_fp)
    return res

def get_config(path, use_defaults=True):
    res = ConfigParser.ConfigParser(CONFIG_DEFAULTS, dict_type = MultiOrderedDict)

    try:
        res.read(path)
    except ConfigParser.MissingSectionHeaderError:
        res = add_missing_header(path)
    except AttributeError:
        res = add_missing_header(path)

    if not res.has_section('settings'):
        res.add_section('settings')
    return res

def extract_mod_paths_morrowind(modlist, path):
    ind = 0
    content = []
    while True:
        key = 'GameFile' + str(ind)
        if modlist.has_option('Game Files', key):
            content.append(modlist.get('Game Files', key))
        else:
            break
        ind += 1
    data_path = os.path.join(os.path.dirname(path), 'Data Files')
    content = map(lambda x: os.path.join(data_path, x), content)
    return content
        
def extract_mod_paths_openmw(modlist):
    content = modlist.get('settings', 'content')
    content = content.split('\n')
    data_dirs = modlist.get('settings', 'data').split('\n')
    data_dirs = map(lambda x: x.strip('"'), data_dirs)
    data_dirs = map(lambda x: os.path.abspath(x), data_dirs)

    res = []
    for c in content:
        full_path = ''
        for d in data_dirs:
            flist = ut.get_file_list(d)
            flist = map(lambda x: os.path.basename(x), flist)
            if c in flist:
                full_path = os.path.join(d, c)
        if not os.path.exists(full_path):
            print 'Warning: could not find ' + full_path
        res.append(full_path)
    return res

def extract_mod_paths(modlist, path):
    if modlist.has_option('settings', 'content'):
        return extract_mod_paths_openmw(modlist)
    if modlist.has_option('Game Files', 'GameFile0'):
        return extract_mod_paths_morrowind(modlist, path)
    return None

options = get_config(args.input_file[0])
options.get('settings', 'process_npcs')
modlist_path = os.path.abspath(os.path.expanduser(options.get('settings', 'modlist_path')))
modlist = get_config(modlist_path, use_defaults=False)
mod_paths = extract_mod_paths(modlist, modlist_path)
