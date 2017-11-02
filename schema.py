from parameters import *
import utility as ut
import index_data as idata
import esm

import struct
import os

SCHEME_DIR = os.path.abspath('data/schema')

scheme_files = ut.get_file_list(SCHEME_DIR)

scheme_data_mappings= {
        'float' : 'f',
        'long' : 'i',
        'short' : 'h',
        'longflag' : 'i',
        'byte' : 'b',
        }
input_data_mappings = {
        'float' : 'f',
        'long' : 'f',
        'short' : 'f',
        'longflag' : 'i',
        'byte' : 'b',
        }
key_type_functions = {
        'f' : float,
        'i' : int,
        'h' : int,
        'b' : int,
        }

output_data_mappings = scheme_data_mappings

scheme_data = {}

def read_scheme(data):
    res = {}
    scheme = []
    key_types = {}
    for line in data:
        line = line.split()
        scheme.append(line[1])
        key_types[line[1]] = line[0]
    record_unpack_string = ""
    for key in scheme:
        key_type = key_types[key]
        record_unpack_string += scheme_data_mappings[key_type]
    res['scheme'] = scheme
    res['key_types'] = key_types
    res['record_unpack_string'] = record_unpack_string
    return res

def read_subscheme(data):
    res = []
    for line in data:
        line = line.split()
        for x in line:
            res.append(x)
    return res

for s_file in scheme_files:
    name = os.path.basename(s_file)
    data = ut.read_newline_sep(s_file)
    scheme_data[name] = read_scheme(data[0])
    scheme_data[name]['subschema'] = []
    if (len(data) > 1):
        for d in data[1:]:
            scheme_data[name]['subschema'].append(read_subscheme(d))

def decode_subrecord(subr, t):
    if t not in scheme_data: return None
    res = {}
    raw_data = ''
    try:
        raw_data = struct.unpack('<' + scheme_data[t]['record_unpack_string'], subr)
    except struct.error:
        for s in scheme_data:
            if t in s:
                try: 
                    t = s
                    raw_data = struct.unpack('<' + scheme_data[t]['record_unpack_string'], subr)
                except struct.error: 
                    continue
    index = 0
    for key in scheme_data[t]['scheme']:
        key_type = scheme_data[t]['key_types']
        res[key] = raw_data[index]
        index += 1
    return res

def decode_all_subrecords(rec):
    new_data = {}
    for subr_type, subr in rec.iteritems():
        if subr_type in scheme_data:
            new_data.update(decode_subrecord(subr, subr_type))
    rec.update(new_data)

def encode_all_subrecords(rec):
    new_data = {}
    for subr_type, subr in rec.iteritems():
        if subr_type in scheme_data:
            new_data[subr_type] = encode_subrecord(rec, subr_type)
    rec.update(new_data)

def find_scheme(rec):
    for sname, scheme in scheme_data.iteritems():
        for s in scheme['scheme']:
            if s not in rec:
                continue
            return sname
    return False
        
def encode_subrecord(rec, t):
    if t not in scheme_data: return None
    res = ""

    for s in scheme_data[t]['scheme']:
        data_type = scheme_data_mappings[scheme_data[t]['key_types'][s]]
        try:
            res += struct.pack('<'+data_type, rec[s])
        except struct.error:
            z = idata.get(rec[s], s+'s')
            res += struct.pack('<'+data_type, z)
        except KeyError:
            return encode_subrecord(rec, find_scheme(rec))
    return res
            
def encode_plaintext(rec, t):
    if t not in scheme_data: return None
    res = ''
    for key in scheme_data[t]['scheme']:
        key_type = scheme_data[t]['key_types']
        res += key + ' ' + str(rec[key]) + '\n'
    return res

def decode_plaintext_entry(x, t=None):
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            if not t: return None
            index_key = t + 's'
            if index_key in idata.index_data:
                return idata.get(x, index_key)
            else:
                return None

def list_reduce(d):
    res = []
    for x in d:
        x = x.split()
        if len(x) == 1: res += x
        else:
            for y in x:
                res += list_reduce([y])
    return res

def decode_plaintext(data, t):
    if len(data) == 0: return {}
    res = {}
    data = list_reduce(data)
    #if not isinstance(data, list): # turn the data into a list of numbers
        #data = data.replace('\n', ' ')
        #data = data.split()


    scheme = list(scheme_data[t]['scheme'])
    if not len(scheme) == len(data):
        for subscheme in scheme_data[t]['subschema']:
            if len(subscheme) == len(data):
                scheme = subscheme

    for d in data:
        if not ut.is_numeric(d):
            for s in scheme:
                z = decode_plaintext_entry(d, s)
                if z:
                    res[s] = z
                    print scheme
                    scheme.remove(s)
    ind = 0
    for s in scheme:
        res[s] = decode_plaintext_entry(data[ind], s)
        ind += 1

    return res

def record_unpack_schema(rec):
    new_data = []
    for key, subr in rec.iteritems():
        if key in scheme_data:
            new_data.append(decode_subrecord(subr, key))
    for n in new_data: rec.update(n)

def record_repack_schema(rec):
    new_data = {}
    for key in rec:
        if key in scheme_data:
            new_data[key] = encode_subrecord(rec, key)
    rec.update(new_data)

#for n, r in esm.test_recs['MGEF'].iteritems():
if 0:
    record_unpack_schema(r)
    r['cost'] = 555.5
    record_repack_schema(r)
    record_unpack_schema(r)
    new_data = {}
    for x, y in r.iteritems():
        d = decode_subrecord(y, x)
        if d:
            new_data.update(d)
            z = encode_subrecord(d, 'MEDT')
            decode_subrecord(z, 'MEDT')
    r.update(new_data)

#print decode_plaintext("illu 1 0 0 0 0 0 0 0", "MEDT")
