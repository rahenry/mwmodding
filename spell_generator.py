import random
import subprocess
import os
import re
import struct

PREFIX = "spellmod"
NULL = '\x00'

index_data_files = ['data/magic_effects', 'data/attributes', 'data/skills']
index_data = {}
for ind in index_data_files:
    name = ind.split('/')[-1]
    index_data[name] = {}
    f = open(ind)
    for l in map(lambda x: x.split(), f.readlines()):
        index_data[name][l[0]] = int(l[1])
index_data["ranges"] = {
        'Self' : 0,
        'Touch' : 1,
        'Target' : 2
        }

input_files = {
        "/home/rah/mwmodding/spells":True
        }

raw_data = {}

def int1(z):
    return struct.pack('<b', int(z))

def int2(z):
    return struct.pack('<h', int(z))

def int4(z):
    return struct.pack('<i', int(z))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def extract_effect(data):
    ef = {}
    ef["name"] = data[0]
    ef["range"] = data[1]
    ef["area"] = data[2]
    if (len(data) == 4 or len(data) == 6):
        ef["duration"] = data[3]
    else:
        ef["duration"] = 'a'
    if (len(data) == 5 or len(data) == 6):
        z = 0
        if (len(data) == 6): z = 1
        ef["min"] = data[3+z]
        ef["max"] = data[4+z]
    return ef

def extract_spell(data):
    sp = {}
    sp["name"] = data[0]
    sp["cost"] = data[1]
    effect_indices = []
    sp["effects"] = []

    sp["autocalc"] = False
    sp["pcstart"] = False
    sp["always"] = False

    i = 2
    if ("autocalc" in data):
        i += 1
        sp["autocalc"] = True
    if ("pcstart" in data):
        i += 1
        sp["pcstart"] = True
    if ("always" in data):
        i += 1
        sp["always"] = True

    c = 0
    i0 = i
    while (True):
        if (not is_number(data[i]) and c >= 2 and data[i] != "a"):
            c = 0
            sp["effects"].append(extract_effect(data[i0:i]))
            i0 = i

        if (data[i] == "end"):
            break

        i = i+1
        c = c+1
    return sp

spells = []
for inp in input_files:
    f = open(inp)
    data = f.read().splitlines()
    f.close()
    i = 0
    i0 = 0
    while (i < len(data)):
        if (data[i] == "end"):
            spells.append(extract_spell(data[i0:(i+1)]))
            i0 = i+2
            i += 2
        i += 1

def encode_record(name, data):
    res = name
    res += int4(len(data))
    res += int4(0)
    res += int4(0)
    res += data
    return res

def encode_subrecord(name, data):
    res = name
    res += int4(len(data))
    res += data
    return res

def encode_enam(en):
    res = ""
    eff = en['name'].split()
    effid = int2(index_data["magic_effects"][eff[0]])
    skillid = int1(-1)
    attid = int1(-1)
    if (len(eff)==2):
        if (eff[1] in index_data["attributes"]):
            attid = int1(index_data["attributes"][eff[1]])
        if (eff[1] in index_data["skills"]):
            skillid = int1(index_data["skills"][eff[1]])
    res += effid
    res += skillid
    res += attid
    res += int4(index_data["ranges"][en["range"]])
    res += int4(en["area"])
    res += int4(en["duration"])
    res += int4(en["min"])
    res += int4(en["max"])
    return res

def encode_SPEL(sp):
    res = ""
    res += encode_subrecord("NAME", PREFIX + '_' + sp["name"].lower()+NULL)
    res += encode_subrecord("FNAM", sp["name"]+NULL)
    flags = 0
    if (sp["autocalc"]): flags += 1
    if (sp["pcstart"]): flags += 2
    if (sp["always"]): flags += 4
    res += encode_subrecord("SPDT", int4(0) + int4(sp["cost"]) + int4(flags))
    for ef in sp["effects"]:
        res += encode_subrecord("ENAM", encode_enam(ef))
    
    return encode_record("SPEL", res)

def encode_TES3(recs):
    res = ""
    ver = struct.pack('<f', 1.2)
    file_type = struct.pack('4s', "")
    company = struct.pack('32s', "rah")
    desc = struct.pack('256s', "spell mod")
    res += encode_subrecord("HEDR", ver + file_type + company + desc + int4(len(recs)))
    res += encode_subrecord("MAST", "Morrowind.esm"+NULL)
    res += encode_subrecord("DATA", struct.pack('<q', 5))
    return encode_record("TES3", res)

recs = []
for s in spells:
    recs.append(encode_SPEL(s))

out = open("test.esp", 'w+')
out.write(encode_TES3(recs))
for r in recs:
    out.write(r)
