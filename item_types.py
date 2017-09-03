from parameters import *
import utility as ut
import index_data as idata
import esm

import struct
import os
import schema
import utility as ut
import materials as mat


input_dir = os.path.abspath("content/item_types")
input_files = ut.get_file_list(input_dir)
item_types = {}

for f in input_files:
    data = ut.read_newline_sep(f)
    rec_type = (os.path.basename(f)).split('_')[0]
    item_types[rec_type] = {}
    for d in data:
        schemename = rec_type + '_type'
        t = {}
        name = ut.reductions(d[0])
        if rec_type == 'WEAP': d = d[1:]

        if (len(d) > 1):
            t = schema.decode_plaintext(d, schemename)
        item_types[rec_type][name] = t

#ITEM_CLASSES = ['ARMO', 'WEAP']
ITEM_CLASSES = ['WEAP']
MAPPING_TYPES = ['MODL']
type_mappings = {}
recs = {}
for item_class in ITEM_CLASSES:
    recs[item_class] = {}
    for item_name, item in esm.records_original[item_class].iteritems():
        if 'FNAM' in item:
            recs[item_class][item_name] = item

for item_class in ITEM_CLASSES:
    itypes = item_types[item_class]
    mats = mat.materials[item_class]
    items = recs[item_class]
    for item_name, item in items.iteritems():
        mats_found = set([])
        types_found = set([])
        for subr_name, subr in item.iteritems():
            if isinstance(subr, list): continue
            for m in mats:
                if m in ut.reductions(subr):
                    mats_found.add(m)
            if item_class != 'ARMO':
                for t in itypes:
                    if t in ut.reductions(subr):
                        types_found.add(t)
        mat = None
        typ = None
        if len(mats_found) == 1:
            mat = mats_found.pop()
        if len(types_found) == 1:
            typ = types_found.pop()
        if item_class == 'ARMO':
            1
        item['material'] = mat
        item['type'] = typ
        if mat and typ:
            type_id = (item_class, mat, typ)
            if type_id in type_mappings:
                # prefer examples without enchantments or scripts
                for k in ['ENAM', 'SCRI']:
                    if k in type_mappings[type_id] and k not in item:
                        type_mappings[type_id] = item
            else: type_mappings[type_id] = dict(item)
            for mtype in MAPPING_TYPES:
                if mtype in item:
                    type_mappings[item[mtype]] = type_id

    for item_name, item in items.iteritems():
        if not item['material'] or not item['type']:
            for mtype in MAPPING_TYPES:
                if mtype in item and item[mtype] in type_mappings:
                        x = type_mappings[item[mtype]]
                        item['material'], item['type'] = x[1], x[2]

    for item_name, item in items.iteritems():
        if not item['material'] or not item['type']:
            s = '%-40s %-10s %-10s' % (item['FNAM'], item['material'], item['type'])
            #print s






