from parameters import *
import utility as ut
import index_data as idata
import esm
import struct
import schema


mgefs = {}
idata.index_data['mgef_to_school'] = {}
for name, mgef in esm.records_original['MGEF'].iteritems():
    mgefs[name] = mgef
    mgefs[name].update(schema.decode_subrecord(mgefs[name]['MEDT'], 'MEDT'))
    index = idata.get(name, 'magic_effects')
    idata.index_data['mgef_to_school'][index] = mgefs[name]['school']


