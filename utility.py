from parameters import *
import struct
import os
def is_numeric(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def get_file_list(base_path):
    res = []
    for fname in os.listdir(base_path):
        path = os.path.join(base_path, fname)
        if os.path.isdir(path): continue
        res.append(path)
    return res

def reductions(x):
    for r in REDUCTIONS:
        x = r(x)
    return x

def read_newline_sep(file_name):
    SECRET_STRING = 'LDSKJF23jnfjsdflj399'
    f = open(file_name)
    data = f.read()
    f.close()
    data = data.replace('\n\n', '\n'+SECRET_STRING)
    data = data.split(SECRET_STRING)
    data = map(lambda x: x.split('\n')[:-1], data)

    removes = [[''], []]
    for r in removes:
        while r in data:
            data.remove(r)

    for x in data:
        if ('#') in x[0]: #commenting
            data.remove(x)
            continue
    return data
