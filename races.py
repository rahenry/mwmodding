import mwdata
import struct
import index_data

input_files = ["input_data/races"]

raw_data = []
for inp in input_files:
    raw_data += mwdata.read_newline_separated(inp)

races = {}
def process_races(records):
    for name, race_orig in records['RACE'].iteritems():
        for race_data in raw_data:
            ident = race_data[0].split()[0]
            if (ident in name.lower()):
                races[name] = process_race_data(name, race_orig, race_data)

def process_race_data(name, orig, d):
    new_race = orig
    new_race['FNAM'] = d[0].split()[-1]

    skil = d[2].split()
    SKIL = ""
    for i in range(7):
        if (i * 2 >= len(skil)):
            SKIL += struct.pack('<i', 0)
            SKIL += struct.pack('<i', 0)
        else:
            skill_id = index_data.get_index(skil[i*2], "skills")
            SKIL += struct.pack('<i', skill_id)
            SKIL += struct.pack('<i', int(skil[i*2+1]))

    attr = d[1].split()
    ATTR = ""
    for a in attr:
        ATTR += struct.pack('<i', int(a))
        ATTR += struct.pack('<i', int(a))

    new_race["RADT"] = SKIL + ATTR + orig["RADT"][0][-12:]


    return new_race





