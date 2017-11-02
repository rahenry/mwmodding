from parameters import *
import utility as ut
import index_data as idata
import esm
import struct
import schema
import os


reference_icons = {}
idata.index_data['mgef_to_school'] = {}
for name, mgef in esm.records_original['MGEF'].iteritems():
    mgef['icon_base'] = os.path.abspath('data/icons/' + mgef['ITEX'][0:-1].lower().replace('.tga', '.dds').replace('\\', '/'))
    index = idata.get(name, 'magic_effects')
    mgef.update(schema.decode_subrecord(mgef['MEDT'], 'MEDT'))
    idata.index_data['mgef_to_school'][index] = mgef['school']
    if mgef['school'] not in reference_icons:
        reference_icons[mgef['school']] = mgef['icon_base']


# data/icons/
# x.replace(.tga, .dds)
