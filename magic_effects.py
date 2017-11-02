from parameters import *
import utility as ut
import index_data as idata
import esm
import struct
import schema
import os
import outputs
import colour_converter

icon_dir = os.path.abspath('output/icons')
if not os.path.exists(icon_dir):
    os.makedirs(icon_dir)

reference_icons = {}
idata.index_data['mgef_to_school'] = {}
for name, mgef in esm.records_original['MGEF'].iteritems():
    mgef['icon_base'] = os.path.abspath('data/icons/' + mgef['ITEX'][0:-1].lower().strip(NULL).replace('.tga', '.dds').replace('\\', '/'))
    index = idata.get(name, 'magic_effects')
    mgef.update(schema.decode_subrecord(mgef['MEDT'], 'MEDT'))
    mgef['name'] = name
    idata.index_data['mgef_to_school'][index] = mgef['school']
    if mgef['school'] not in reference_icons:
        reference_icons[mgef['school']] = mgef['icon_base']

input_dir = os.path.abspath('content/magic_effects')
input_files = ut.get_file_list(input_dir)

def make_new_icon(mgef):
    icon_path = ('icons/' + mgef['name'] + '.dds')
    output = os.path.abspath('output'+'/'+icon_path)
    source = mgef['icon_base']
    obj = reference_icons[mgef['school']]
    colour_converter.recolour(source, obj, output)
    source = source.replace('tx_', 'b_tx_')
    obj = obj.replace('tx_', 'b_tx_')
    output = output.replace('tx_', 'b_tx_')
    colour_converter.recolour(source, obj, output)
    return output


mgefs_new = {}
for f in input_files:
    data = ut.read_newline_sep(f)
    for d in data:
        name = d[0]
        if name not in esm.records_original['MGEF']:
            continue
        else:
            mgefs_new[name] = esm.records_original['MGEF'][name]
        mgef = mgefs_new[name]
        school_old = mgef['school']
        if len(d) > 1:
            mgef.update(schema.decode_plaintext(d[1:], 'MEDT'))
        schema.encode_all_subrecords(mgef)

        if school_old != mgef['school']:
            mgef['ITEX'] = make_new_icon(mgef)

output_names = ['spellmod', 'everything']
outputs.update({'MGEF':mgefs_new}, output_names)



# data/icons/
# x.replace(.tga, .dds)
