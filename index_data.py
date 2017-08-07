index_data_files = ['data/magic_effects', 'data/attributes', 'data/skills', 'data/schools']
index_data = {}
for ind in index_data_files:
    name = ind.split('/')[-1]
    index_data[name] = {}
    f = open(ind)
    for l in map(lambda x: x.split(), f.readlines()):
        index_data[name][l[0]] = int(l[1])
index_data["ranges"] = {
        'Self' : 0,
        'Touch' : 1,
        'Target' : 2
        }

reverse_index_data = {}
for name in index_data:
    reverse_index_data[name] = {}
    for key in index_data[name]:
        reverse_index_data[name][index_data[name][key]] = key

def get_index(key, data_type):
    return int(index_data[data_type][key])

def get_key(index, data_type):
    return reverse_index_data[data_type][index]

