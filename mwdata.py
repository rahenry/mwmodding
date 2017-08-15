import struct 
import index_data
import os

NULL = '\x00'

openmw_data_dir = os.path.expanduser("~/.local/share/openmw/data")
data_files = map(lambda x: openmw_data_dir + '/' + x, ["Morrowind.esm", "Tribunal.esm", "Bloodmoon.esm"])

record_type_orderings = {}
id_types = ['FNAM', 'NAME', 'INDX', 'SCHD']

def extract_subrecords(d):
    res = {}
    i = 0
    while (i < len(d)):
        name = d[i:i+4]
        s = struct.unpack('<i', d[i+4:i+8])[0]
        if (not name in res): res[name] = []
        res[name].append("".join(d[i+8:i+8+s]))
        i += 8+s
    return res

def extract_type_ordering(d):
    res = []
    i = 0
    while (i < len(d)):
        name = d[i:i+4]
        s = struct.unpack('<i', d[i+4:i+8])[0]
        if (not name in res): res.append(name)
        i += 8+s
    return res

def get_subrecord(name, r, i=0):
    return r[name][i]

def extract_records(record_types_of_interest):
    record_types_of_interest.append("TES3")
    records = {}
    for r in record_types_of_interest:
        records[r] = {}
        record_type_orderings[r] = []
    data_raw = ""
    for d in data_files:
        f = open(d)
        data_raw += f.read()

    i = 0
    while (i < len(data_raw)):
        name = data_raw[i:i+4]
        s = struct.unpack('<i', data_raw[i+4:i+8])[0]
        id_index = 0
        if (name in record_types_of_interest):
            subr = extract_subrecords(data_raw[i+16:i+s+16])

            new_id = id_index
            id_index += 1
            found_id = False
            if (name == "MGEF"):
                new_id = index_data.convert_INDX(get_subrecord("INDX", subr))
                found_id = True
            else:
                for id_type in id_types:
                    if (id_type in subr):
                        new_id = get_subrecord(id_type, subr)
                        found_id = True
                        break
            if (not found_id and not (name == "TES3")): 
                print subr
                print "OH NO"
            records[name][new_id] = subr

            type_ord = extract_type_ordering(data_raw[i+16:i+s+16])
            for j in range(len(type_ord)):
                if (not type_ord[j] in record_type_orderings[name]):
                    record_type_orderings[name].insert(j+1, type_ord[j])
        i += s+16
    return records

def encode_record(name, d):
    res = ""
    for subr in record_type_orderings[name]:
        if subr in d:
            for s in d[subr]:
                res += subr
                res += struct.pack('<i', len(s))
                res += s
    return name + struct.pack('<i', len(res)) + struct.pack('<i', 0) + struct.pack('<i', 0) + res

def read_long(record, key):
    return int(struct.unpack('<i', record[key][0][0:4])[0])

def read_file_path(record, key):
    return record[key][0][0:-1].replace('\\', '/')

def encode_path(path):
    return path.replace('/', '\\') + NULL

def read_icon_path(record):
    x = "data/icons/" + read_file_path(record, 'ITEX')
    x = x.replace(".tga", ".dds").lower()
    return x

def read_newline_separated(file_name):
    f = open(file_name)
    d = f.read()
    d = d.split('\n\n')
    d = map(lambda x: x.split('\n'), d)
    for z in d:
        if z[-1] == '':
            z = z[0:-1]
    #return d
    g = open(file_name)
    d = g.read()
    d = d.replace('\n\n', '\nXXXXX')
    d = d.split('XXXXX')
    d = map(lambda x: x.split('\n')[:-1], d)

    for x in d:
        if (x == []):
            d.remove([])
    return d

def write_esp(records):
    data = ""
    for record_type in records:
        for r in records[record_type].itervalues():
            data += encode_record(record_type, r)
    tes3 = {}
    ver = struct.pack('<f', 1.2)
    file_type = struct.pack('4s', "")
    company = struct.pack('32s', "rah")
    desc = struct.pack('256s', "spell mod")
    tes3["HEDR"] = [ver + file_type + company + desc + struct.pack('<i', len(data))]
    tes3["MAST"] = ["Morrowind.esm"+NULL]
    tes3["DATA"] = [struct.pack('<q', 5)]
    res = encode_record("TES3", tes3) + data

    return res

def unpack_flags(flags):
    s = len(flags) * 8
    val = struct.unpack('<i', flags)[0]
    res = []
    for i in range(s):
        res.append(0)
    for i in range(s):
        z = 2 ** (s-i-1)
        if val >= z:
            res[i] = 1
            val -= z

    return res

