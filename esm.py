# functions for encoding and decoding ESM data

from parameters import *
import utility as ut
import index_data as idata
import struct


# these subrecords can be used to create a unique identifier
# INDX is also used, see below
id_encoding_types = ['NAME', 'SCHD']
null_terminated_types = ['NAME', 'FNAM']

records_original = {}
record_subrecord_orderings = {}

data_files = []
for f in ut.get_file_list(MW_DATA_PATH):
    if '.esm' in f: data_files.append(f)
#data_files = ["test.esm"]

def make_id(rec, rtype):
    for t in id_encoding_types:
        if t in rec:
            return rec[t].strip(NULL)
    if 'INDX' in rec:
        data_type = ''
        if (rtype == 'MGEF'): data_type = 'magic_effects'
        if (rtype == 'SKIL'): data_type = 'skills'
        ind = struct.unpack('<i', rec['INDX'])[0]
        return idata.get(ind, data_type)
    return None
        
def update_record_subrecord_orderings(subrecord_order, rtype):
    if rtype not in record_subrecord_orderings:
        record_subrecord_orderings[rtype] = subrecord_order
        return
    for j in range(len(subrecord_order)):
        if not subrecord_order[j] in record_subrecord_orderings[rtype]:
            record_subrecord_orderings[rtype].insert(j+1, subrecord_order[j])

def extract_record(d, rtype):
    res = {}
    i = 0
    subrecord_order = []
    while (i < len(d)):
        subr_name = d[i:i+4]
        if not subr_name in subrecord_order: subrecord_order.append(subr_name)
        s = struct.unpack('<i', d[i+4:i+8])[0]
        subr_data = d[i+8:i+8+s]

        # if we're on an armour record and an INDX subrecord, see if there's a BNAM next and if so, just add it to the INDX data
        if (rtype == 'ARMO' and subr_name == 'INDX'):
        #if (0):
            if 'INDX' not in res: res['INDX'] = []
            subr_data = [subr_data, ""]
            offset = i+8+s
            while (True):
                if len(d) > offset+8 and d[offset:offset+4] in ['CNAM', 'BNAM']:
                    bnam_size = struct.unpack('<i', d[offset+4:offset+8])[0]
                    bnam_data = d[offset+8:offset+8+bnam_size]
                    BNAM = d[offset:offset+8+bnam_size]
                    subr_data[1] += BNAM
                    #if d[offset:offset+4] == 'CNAM': print BNAM
                    offset += bnam_size + 8
                    s += bnam_size+8
                    # skip the BNAM record which comes after!
                else:
                    break

        if not subr_name in res: res[subr_name] = subr_data
        else:
            if isinstance(res[subr_name], list): res[subr_name].append(subr_data)
            else: res[subr_name] = [res[subr_name], subr_data]
        i += 8+s
        update_record_subrecord_orderings(subrecord_order, rtype)

    return res

def extract_records():
    for rtype in RECORD_TYPES_OF_INTEREST:
        records_original[rtype] = {}
        record_subrecord_orderings[rtype] = []

    data_raw = ""
    for d in data_files:
        f = open(d)
        data_raw += f.read()
        f.close()

    i = 0
    while (i < len(data_raw)):
        rtype = data_raw[i:i+4]
        rsize = struct.unpack('<i', data_raw[i+4:i+8])[0]

        if rtype in RECORD_TYPES_OF_INTEREST:
            record = extract_record(data_raw[i+16:i+rsize+16], rtype)
            records_original[rtype][make_id(record, rtype)] = record
            
        i += 16+rsize

def encode_subrecord(subr_type, s):
    res = ""
    if isinstance(s, list):
        #print s
        res += encode_subrecord(subr_type, s[0])
        res += s[1]
        return res
    res += subr_type
    if subr_type in null_terminated_types and s[-1] != NULL:
        s += NULL
    res += struct.pack('<i', len(s))
    res += s
    return res

def encode_record(rtype, d):
    res = ""
    d = dict(d)
    # make everything into a list
    for subr_type in record_subrecord_orderings[rtype]:
        if subr_type in d:
            subr = d[subr_type]
            if not isinstance(subr, list): d[subr_type] = [subr]

    for subr_type in record_subrecord_orderings[rtype]:
        if subr_type in d:
            subr = d[subr_type]
            for s in subr:
                res += encode_subrecord(subr_type, s)
    return rtype + struct.pack('<iii', len(res), 0, 0) + res

def encode_esp(records):
    data = ""
    for rtype in records:
        if rtype == 'TES3': continue
        for r in records[rtype].itervalues():
            data += encode_record(rtype, r)
    TES3 = {}
    TES3['HEDR'] = struct.pack('<f4s32s256si', 1.2, "", AUTHOR_NAME, MOD_DESCRIPTION, len(data))
    TES3['MAST'] = 'Morrowind.esm'+NULL
    TES3['DATA'] = struct.pack('<q', 5)
    return encode_record('TES3', TES3) + data

def write_esp(records, file_name):
    f = open(file_name, 'w+')
    f.write(encode_esp(records))
    f.close()

extract_records()

#test_recs = dict(records_original)
#test_recs['NPC_'] = {}
#zzz = ['arrille']
#write_esp(test_recs, "recode_test.esp")

