import struct 
from index_data import *
from mwdata import *
from colour_converter import *

NULL = '\x00'

reference_icons = {}
for school in index_data['schools']:
    for mgef in records['MGEF']:
        s = read_long(mgef, 'MEDT')
        if (s == index_data['schools'][school]):
            reference_icons[school] = read_icon_path(mgef)
            break

mgef_data = read_newline_separated("input_data/magic_effects")
mgef_new_records = []
for d in mgef_data:
    name = ""
    for mgef in index_data["magic_effects"]:
        if mgef in d:
            name = mgef
            break
    if (name == ""): continue

    school = ""
    for s in index_data["schools"]:
        if s in d:
            school = s
            break

    for mgef in records['MGEF']:
        INDX = read_long(mgef, 'INDX')
        u = get_index(name, 'magic_effects')
        if (INDX == get_index(name, 'magic_effects')):
            s = read_long(mgef, 'MEDT')

            if (s != get_index(school, 'schools')):
                # we've redefined this effect's school!
                output_file = "icons/" + name.lower() + ".dds"
                mgef_new_records.append(dict(mgef))
                mgef_new_records[-1]['ITEX'] = [encode_path(output_file)]

                source_file = read_icon_path(mgef)
                objective_file = reference_icons[school]
                recolour(source_file, objective_file, output_file)

                source_file = source_file.replace("tx_", "b_tx_")
                objective_file = objective_file.replace("tx_", "b_tx_")
                output_file = "icons/b_" + name.lower() + ".dds"
                recolour(source_file, objective_file, output_file)

f = open("test3.esp", 'w+')
f.write(write_esp({"MGEF" : mgef_new_records}))
