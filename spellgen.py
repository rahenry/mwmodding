import index_data
import mwdata
import struct
import math

PREFIX = "spellmod"
NULL = '\x00'
INSTANCES_MIN_BASE = 5
INSTANCES_MAX_BASE = 1000
DURATION_EFFICIENCY_FACTOR = 1.0
AREA_EFFICIENCY_FACTOR = -0.2*math.log(0.75)
SDEV_EFFICIENCY_MAX = 1.1
SUCCESS_THRESHHOLD = 0.8

input_files = ["input_data/spells"]

raw_data = []
for inp in input_files:
    raw_data += mwdata.read_newline_separated(inp)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def convert_skill_to_willpower(s):
    pts = ((35., 50.), (100., 105.))
    grad = (pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0])
    c = pts[0][1] - grad * pts[0][0]
    return grad * s + c

def convert_skill_to_luck(s):
    pts = ((35., 40.), (100., 100.))
    grad = (pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0])
    c = pts[0][1] - grad * pts[0][0]
    return grad * s + c

def convert_skill_to_cost(s):
    return 2.*s + 0.2*convert_skill_to_willpower(s) + 0.1*convert_skill_to_luck(s) - SUCCESS_THRESHHOLD * 100. / 1.25

def get_spell_flags(line):
    auto_calc = False
    PC_start = False
    always_succeeds = False
    for x in line:
        x = x.lower()
        if "auto" in x: auto_calc = True
        if "pc" in x or "start" in x: PC_start = True
        if "always" in x or "succ" in x: always_succeeds = True

    return auto_calc * 1 + PC_start * 2 + always_succeeds * 4

def process_npcs(d):
    res = []
    for npc in d:
        res.append(npc)
    return res

def get_power(cost):
    return cost / 3.0

def calc_minmax(mean, sdev):
    return (mean * (1.0 - sdev), mean * (1.0 + sdev))

def duration_efficiency(d):
    res = 1.0
    if (d == 0): res = 0.9
    if (d == 2): res = 1.1
    if (d > 2): 
        A = 1.2 / math.log(3.0 * DURATION_EFFICIENCY_FACTOR)
        res = A * math.log(d*DURATION_EFFICIENCY_FACTOR)
    return res

def area_efficiency(a):
    return math.exp(AREA_EFFICIENCY_FACTOR * a)

def sdev_efficiency(sdev):
    return 1.0 + sdev * (SDEV_EFFICIENCY_MAX - 1.0)

def calc_mags(effect_name, eff, sdev, duration, area, cost):
    eff *= duration_efficiency(int(duration)) * area_efficiency(int(area)) * sdev_efficiency(sdev)
    power = eff * get_power(int(cost))
    return map(int, calc_minmax(power, sdev))
    
def process_ENAM(d, cost, flags):
    res = ""

    effect_name = index_data.get_alias(d[0], "magic_effects")
    effect_id = index_data.get_index(effect_name, "magic_effects")

    offset = 0
    attr_id = -1
    if ("attribute" in effect_name):
        attr_id = index_data.get_index(d[1], "attributes")
        offset = 1

    skill_id = -1
    if ("skill" in effect_name):
        skill_id = index_data.get_index(d[1], "skills")
        offset = 1

    res += struct.pack("<h", effect_id)
    res += struct.pack("<b", skill_id)
    res += struct.pack("<b", attr_id)

    ran = "self"
    calc_method = "minmax"
    d_numbers = []
    for x in d[1+offset:]:
        if is_number(x):
            d_numbers.append(float(x))
        elif (x == '!'):
            calc_method = "effdev"
        else:
            r = index_data.get_alias(x, "ranges")
            if r: ran = r

    magmin = 1
    magmax = 1
    area = 0
    duration = 0
    if ("buff" in flags):
        duration = 999

    N = len(d_numbers)
    if (calc_method == "minmax"):
        if (N == 1):
            magmin = d_numbers[0]
            magmax = d_numbers[0]
        if (N == 2):
            magmin = d_numbers[0]
            magmax = d_numbers[0]
            duration = d_numbers[1]
        if (N == 3):
            magmin = d_numbers[0]
            magmax = d_numbers[1]
            duration = d_numbers[2]
        if (N >= 4):
            magmin = d_numbers[0]
            magmax = d_numbers[1]
            duration = d_numbers[2]
            area = d_numbers[3]
    else: # calc_method == effdev
        eff = 1.0
        sdev = 0.0
        if (N == 1):
            eff = d_numbers[0]
        if (N == 2):
            eff = d_numbers[0]
            duration = d_numbers[1]
        if (N == 3):
            eff = d_numbers[0]
            sdev = d_numbers[1]
            duration = d_numbers[2]
        if (N >= 4):
            eff = d_numbers[0]
            sdev = d_numbers[1]
            duration = d_numbers[2]
            area = d_numbers[3]

        (magmin, magmax) = calc_mags(effect_name, eff, sdev, duration, area, cost)

    res += struct.pack("<i", index_data.get_index(ran, "ranges"))
    res += struct.pack("<i", area)
    res += struct.pack("<i", duration)
    res += struct.pack("<i", magmin)
    res += struct.pack("<i", magmax)

    return res

def process_spell(d):
    first_line = d[0].split()
    cost = 5
    
    name = ''
    z = first_line[-1]
    if (is_number(z)): 
        cost = int(z)
        name = d[0][0:-len(z)-1]
    elif (is_number(z[:-1]) and z[-1] == "s"):
        skill = int(z[:-1])
        cost = convert_skill_to_cost(skill)
        name = d[0][0:-len(z)-1]
    else:
        name = d[0]
    
    print name
    if (cost < 1): cost = 1

    
    second_list = d[1].split()
    second_list_numbers = []
    flags = []
    for x in second_list:
        if is_number(x): second_list_numbers.append(int(x))
        else: flags.append(x.lower())

    typeflag = 0
    for t in index_data.index_data["spell_types"]:
        if t in flags:
            typeflag = index_data.get_index(t, "spell_types")

    
    instances = [INSTANCES_MIN_BASE, INSTANCES_MAX_BASE]
    if (len(second_list_numbers) > 0): instances[0] = second_list_numbers[0]
    if (len(second_list_numbers) > 1): instances[1] = second_list_numbers[1]

    res = {}
    res['NAME'] = [name.lower() + NULL]
    res['FNAM'] = [name + NULL]
    res['SPDT'] = [struct.pack('<i', typeflag) + struct.pack('<i', cost) + struct.pack('<i', get_spell_flags(second_list))]
    res['ENAM'] = []
    res['npcs'] = []
    res['instances'] = instances
    res['flags'] = flags
    res['flags'] = flags

    for line in d[2:]:
        entries = line.split()
        if entries[0].lower() == "npcs":
            res['npcs'] += process_npcs(entries[1:])
        else: 
            res['ENAM'].append(process_ENAM(entries, cost, flags))

    return res

spells = {}
for r in raw_data:
    if (r != ['']):
        s = process_spell(r)
        spells[mwdata.get_subrecord('NAME', s)[0:-1]] = s
        


def test1():
    l = range(0, 10)
    print l
    for x in l:
        print duration_efficiency(x)
