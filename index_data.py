from parameters import *
import utility as ut
import struct
import os

# provides mappings for morrowind's enumerated data types such as magic effects

index_data_dir = 'data/index_data'
index_data_dir = os.path.abspath(index_data_dir)
index_data = {}
aliases = {}

index_data_files = ut.get_file_list(index_data_dir)

def try_subkeys(k, ref):
    k = ut.reductions(k)
    if not isinstance(ref, dict):
        ref = index_data[ref]

    for key in ref:
        if isinstance(key, str):
            if k in key:
                return key
    return None

def complete_key(k, data_type):
    return find_key(find_key(k, data_type), data_type)

def find_key(k, data_type):
    if k in index_data[data_type]:
        return k
    if not isinstance(k, str):
        return None
    if k in aliases:
        k = aliases[k]
        return find_key(k, data_type)
    z = try_subkeys(k, index_data[data_type])
    if z: return z
    z = try_subkeys(k, aliases)
    if z: return z
    return None

def process_index_data(data_file):
    name = os.path.basename(data_file)
    index_data[name] = {}
    f = open(data_file)
    for l in f.readlines():
        l = l.split()
        l[0] = ut.reductions(l[0])
        l[1] = int(l[1])
        index_data[name][l[0]] = l[1]
        index_data[name][l[1]] = l[0]

def process_alias_data(data_file):
    f = open(data_file)
    for l in f.readlines():
        l = l.split()
        l = map(ut.reductions, l)
        for alias in l[1:]:
            aliases[alias] = l[0]

for data_file in index_data_files:
    name = os.path.basename(data_file)
    if not 'alias' in data_file:
        process_index_data(data_file)
    else:
        process_alias_data(data_file)

def get(x, data_type):
    x = find_key(x, data_type)
    return index_data[data_type][x]
