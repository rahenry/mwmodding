import struct 
import os

index_data_files = ['data/magic_effects', 'data/attributes', 'data/skills', 'data/schools', 'data/ranges', 'data/spell_types']
index_data = {}

aliases = {}

for ind in index_data_files:
    name = ind.split('/')[-1]
    name = name.lower()
    index_data[name] = {}
    f = open(ind)
    for l in map(lambda x: x.split(), f.readlines()):
        index_data[name][l[0].lower()] = int(l[1])
    f.close()

    aliases[name] = {}
    for x in index_data[name]:
        aliases[name][x] = x
    alias_file = ind + "_aliases"
    if (os.path.isfile(alias_file)):
        f = open(alias_file)
        for l in f.readlines():
            l = l.split(' ')
            key = l[0].lower()
            if key in index_data[name]:
                for alias in l[1:]:
                    alias = alias.strip('\n')
                    aliases[name][alias] = key

reverse_index_data = {}
for name in index_data:
    reverse_index_data[name] = {}
    for key in index_data[name]:
        reverse_index_data[name][index_data[name][key]] = key

def get_data(name):
    return index_data[name]

def get_index(key, data_type):
    key = get_alias(key, data_type)
    if key in index_data[data_type]:
        return int(index_data[data_type][key])
    else: return -1

def get_key(index, data_type):
    return reverse_index_data[data_type][index]

def convert_INDX(INDX):
    return get_key(struct.unpack('<i', INDX)[0], "magic_effects")

def get_alias(key, data_type):
    try:
        return aliases[data_type][key]
    except KeyError:
        for k in aliases[data_type]:
            if k.startswith(key):
                return aliases[data_type][k]
        for k in aliases[data_type]:
            if key in k:
                return aliases[data_type][k]
    return None

