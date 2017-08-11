import struct 
import index_data
import mwdata
import colour_converter

NULL = '\x00'

def process_mgefs(records):
    schools = index_data.get_data('schools')
    reference_icons = {}
    for school in schools:
        for ind, d in records['MGEF'].iteritems():
            s = mwdata.read_long(d, 'MEDT')
            if (s == schools[school]):
                reference_icons[school] = mwdata.read_icon_path(d)
                break

    mgef_data = mwdata.read_newline_separated("input_data/magic_effects")
    mgef_new_records = {}
    for d in mgef_data:
        name = ""
        for mgef in index_data.get_data("magic_effects"):
            if mgef in d:
                name = mgef
                break
        if (name == ""): continue

        school = ""
        for s in schools:
            if s in d:
                school = s
                break

        for ind, mgef in records['MGEF'].iteritems():
            INDX = mwdata.read_long(mgef, 'INDX')
            u = index_data.get_index(name, 'magic_effects')
            if (INDX == index_data.get_index(name, 'magic_effects')):
                s = mwdata.read_long(mgef, 'MEDT')

                if (s != index_data.get_index(school, 'schools')):
                    # we've redefined this effect's school!
                    output_file = "icons/" + name.lower() + ".dds"
                    mgef_new_records[ind] = dict(mgef)
                    mgef_new_records[ind]['ITEX'] = [mwdata.encode_path(output_file)]

                    source_file = mwdata.read_icon_path(mgef)
                    objective_file = reference_icons[school]
                    colour_converter.recolour(source_file, objective_file, output_file)

                    source_file = source_file.replace("tx_", "b_tx_")
                    objective_file = objective_file.replace("tx_", "b_tx_")
                    output_file = "icons/b_" + name.lower() + ".dds"
                    colour_converter.recolour(source_file, objective_file, output_file)

    f = open("test_magic_effects.esp", 'w+')
    f.write(mwdata.write_esp({"MGEF" : mgef_new_records}))
