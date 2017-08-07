import struct 

NULL = '\x00'

openmw_data_dir = "/home/rah/.local/share/openmw/data"
data_files = map(lambda x: openmw_data_dir + '/' + x, ["Morrowind.esm", "Tribunal.esm", "Bloodmoon.esm"])

record_types_of_interest = ['MGEF', 'TES3']
record_type_orderings = {}

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

def extract_records():
    records = {}
    for r in record_types_of_interest:
        records[r] = []
        record_type_orderings[r] = []
    data_raw = ""
    for d in data_files:
        f = open(d)
        data_raw += f.read()

    i = 0
    while (i < len(data_raw)):
        name = data_raw[i:i+4]
        s = struct.unpack('<i', data_raw[i+4:i+8])[0]
        if (name in record_types_of_interest):
            subr = extract_subrecords(data_raw[i+16:i+s+16])
            records[name].append(dict(subr))
            #if (record_type_orderings[name] == []):
                #record_type_orderings[name] = extract_type_ordering(data_raw[i+16:i+s+16])
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

records = extract_records()

def read_long(record, key):
    return int(struct.unpack('<i', record[key][0][0:4])[0])

def read_file_path(record, key):
    return record[key][0][0:-1].replace('\\', '/')

def encode_path(path):
    return path.replace('/', '\\') + NULL

def read_icon_path(record):
    x = "bsa_unpacked/morrowind/icons/" + read_file_path(record, 'ITEX')
    x = x.replace(".tga", ".dds").lower()
    return x

def read_newline_separated(file_name):
    f = open(file_name)
    d = f.read()
    d = d.split('\n\n')
    d = map(lambda x: x.split('\n'), d)
    return d

def write_esp(records):
    data = ""
    for name in records:
        for r in records[name]:
            data += encode_record(name, r)
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

