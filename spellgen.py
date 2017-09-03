from parameters import *
import utility as ut
import index_data as idata
import esm

import struct
import os
import schema
import outputs

input_dir = os.path.abspath("content/spells")
input_files = ut.get_file_list(input_dir)

attack_types = {}
new_spells = {}
buffs = {}
bounds = {}

def skill_to_will(s):
    pts = ((5., 40.), (100., 105.))
    grad = (pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0])
    c = pts[0][1] - grad * pts[0][0]
    return grad * s + c

def skill_to_luck(s):
    pts = ((5., 40.), (100., 100.))
    grad = (pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0])
    c = pts[0][1] - grad * pts[0][0]
    return grad * s + c

def skill_to_cost(s):
    #print s, 2.*s + 0.2*skill_to_will(s) + 0.1*skill_to_luck(s) - SUCCESS_THRESHHOLD * 100. / 1.25
    return 2.*s + 0.2*skill_to_will(s) + 0.1*skill_to_luck(s) - SUCCESS_THRESHHOLD * 100. / 1.25

def make_spell_flags(flags):
    res = 0
    for f in flags:
        f = ut.reductions(f)
        if 'auto' in f: res += 1
        if 'pc' in f or 'start' in f: res += 2
        if 'always' in f or 'succ' in f: res += 4
    return res

def calc_minmax(mean, var):
    if var > 1.0: var = 1.0
    if var < 0.0: var = 0.0
    return (mean * (1.0-var), mean * (1.0+var))

def eff_duration(d):
    res = 1.0
    if (d==0): res = 0.95
    if (d==2): res = 1.05
    if (d > 2):
        A = DURATION_EFFICIENCY_COEF
        res = A * math.log(d * DURATION_EFFICIENCY_FACTOR)
    return res

def eff_area(a):
    if a < 0.9: return 1.0
    if a <= area_efficiency_pts[1][0]+0.1:
        pts = ((1., 1.), area_efficiency_pts[1])
        grad = (pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0])
        c = pts[0][1] - grad * pts[0][0]
        res = a*grad + c
    else:
        res = AREA_EFFICIENCY_COEF * pow(a, -AREA_EFFICIENCY_POWER)
    return res

def eff_var(v):
    return 1.0 + v * (SDEV_EFFICIENCY_MAX - 1.0)

def calc_mag(spell):
    if spell['magic_effect'] in attack_types:
        x = attack_types[spell['magic_effect']]['cost']

    dur = spell['duration']
    if dur < 0.1: dur = 1.0
    spell['power'] = spell['efficiency'] * eff_duration(spell['duration']) * eff_area(spell['area']) * eff_var(spell['variability']) * spell['cost'] * x / SPELL_ATTACK_BASE_COST / dur
    (spell['min'], spell['max']) = calc_minmax(spell['power'], spell['variability'])

def read_attack_types():
    data = ut.read_newline_sep(os.path.abspath('data/spell_attack_types'))
    for d in data:
        attack_types[idata.complete_key(d[0], 'magic_effects')] = schema.decode_plaintext(d[1:], 'spell_attack')

def build_ENAM(d, spell_rec, autobuild):
    res = {}
    d = d.split()

    res['skill'] = -1
    res['attribute'] = -1
    if spell_rec:
        res['name'] = spell_rec['FNAM']
        res['cost'] = spell_rec['cost']

    params = ['range', 'magic_effect', 'skill', 'attribute']
    number_data = []
    for x in d:
        number = ut.is_numeric(x)
        if number: 
            number_data.append(x)
        else:
            for p in params:
                #val = idata.try_subkeys(d, p+'s')
                val = idata.complete_key(x, p+'s')
                if val:
                    res[p] = val
                    break
                    
    try:
        res['magic_effect']
    except KeyError:
        print "magic_effect key error in " + spell_rec['FNAM']

    if 'range' not in res:
        if res['magic_effect'] in attack_types:
            res['range'] = 1 #touch
        else:
            res['range'] = 0 #self

    if autobuild:
        res.update(schema.decode_plaintext(number_data, 'ENAM_subdata_autobuild'))
        if 'efficiency' not in res: res['efficiency'] = 1.0
        if 'variability' not in res: res['variability'] = 0.0
        if not 'duration' in res: res['duration'] = 0
        if not 'area' in res: res['area'] = 0
        calc_mag(res)
    else:
        res.update(schema.decode_plaintext(number_data, 'ENAM_subdata'))

    if not 'min' in res: res['min'] = 1
    if not 'max' in res: res['max'] = res['min']
    if not 'duration' in res: res['duration'] = 0
    if not 'area' in res: res['area'] = 0

    if spell_rec:
        for flag in spell_rec['flags']:
            if 'buff' in flag:
                res['duration'] = 1
        spell_rec['duration'] = res['duration']

    res['mag'] = 0.5 * (res['min'] + res['max'])
    res['school'] = idata.get(idata.get(res['magic_effect'], 'magic_effects'), 'mgef_to_school')

    res['data'] = schema.encode_subrecord(res, 'ENAM')
    return res

def read_spell_plaintext(data):
    res = {}
    flags = []

    data[0] = data[0].split()
    cost = data[0][-1]
    if (ut.is_numeric(cost) or ut.is_numeric(cost[0:-1])):
        data[0].remove(cost)
        if 's' in cost:
            cost = cost.replace('s', '')
            flags.append('skillcalc')
        if 'skillcalc' in flags:
            res['cost'] = skill_to_cost(float(cost))
        else:
            res['cost'] = float(cost)
    else:
        res['cost'] = 1

    name = ' '.join(data[0])
    res['FNAM'] = name
    res['NAME'] = PREFIX + ut.reductions(name)
    res['flags'] = []
    res['schools'] = []

    prefix = ''

    for d in data[1:]:
        if 'flags' in d:
            s = d.split()

            s.remove('flags')
            res['flags'] += s
            data.remove(d)

    res['spell_type'] = 0
    for f in res['flags']:
        spell_type = idata.find_key(f, 'spell_types')
        if spell_type: res['spell_type'] = spell_type
    res['spell_flags'] = make_spell_flags(res['flags'])

    res['ENAM'] = []
    res['enams'] = []
    for d in data[1:]:
        autobuild = False
        if '!' in d:
            d = d.replace('!', '')
            autobuild = True
        new_enam = build_ENAM(d, res, autobuild)
        res['ENAM'].append(new_enam['data'])
        res['enams'].append(new_enam)

    res['SPDT'] = schema.encode_subrecord(res, 'SPDT')

    return res
    
def make_bound_effect(spell):
    res = dict(spell)
    res['spell_type'] = idata.get('ability', 'spell_types')
    res['SPDT'] = schema.encode_subrecord(res, 'SPDT')
    res['NAME'] += '_boundeffect'
    return res

def make_buff_effect(spell):
    res = dict(spell)
    res['spell_type'] = idata.get('ability', 'spell_types')
    res['SPDT'] = schema.encode_subrecord(res, 'SPDT')
    res['NAME'] += '_buffeffect'
    return res

read_attack_types()
for f in input_files:
    data = ut.read_newline_sep(f)
    for d in data:
        new_spell = read_spell_plaintext(d)
        new_spells[new_spell['NAME']] = new_spell
        for flag in new_spell['flags']:
            if 'buff' in flag:
                d = int(flag[4:])
                new_spell['buff_points'] = d
                buff_effect = make_buff_effect(new_spell)
                buffs[new_spell['NAME']+'_buffeffect'] = buff_effect
            if 'bound' in flag:
                bound_effect = make_bound_effect(new_spell)
                bounds[new_spell['NAME']+'_boundeffect'] = bound_effect

tier_cutoffs = [30, 50, 70, 90, 110]
tier_cutoffs = map(skill_to_cost, tier_cutoffs)
def get_tier(spell):
    index = 1
    for t in tier_cutoffs:
        if spell['cost'] < t:
            return index
        index += 1
    return index

def spell_report():
    attack_type_data = {}
    for a in attack_types:
        attack_type_data[a] = {}
        attack_type_data[a]['spells'] = []
    for a in attack_types:
        for spellid, spell in new_spells.iteritems():
            for e in spell['enams']:
                if e['magic_effect'] == a:
                    attack_type_data[a]['spells'].append(spell)
                    continue
    for a in attack_types:
        for i in range(1, 6):
            attack_type_data[a]['T' + str(i)] = 0
        for spell in attack_type_data[a]['spells']:
            tier = get_tier(spell)
            attack_type_data[a]['T'+str(tier)] += 1

    f = open(os.path.abspath('reports/spellgen/attack_types'), 'w+')
    f.write('%-15s ' % '')
    for i in range(1, 6):
        f.write('%5s ' % ('T'+str(i)))
    f.write('\n')
    f.write('\n')

    for a in attack_types:
        f.write('%-15s ' % a)
        for i in range(1, 6):
            f.write('%5i ' % attack_type_data[a]['T'+str(i)])
        f.write('\n')
    f.close()


    for school in range(6):
        school_name = idata.get(school, 'schools')
        res = []
        for spellid, spell in new_spells.iteritems():
            name = spell['FNAM']
            accept = False
            for e in spell['enams']:
                if idata.get(idata.get(e['magic_effect'], 'magic_effects'), 'mgef_to_school') == school:
                    accept = True
            if not accept: continue

            s = spell['FNAM']+ ' ' + str(spell['cost'])
            s = '%-25s' % s
            temp = ''
            if 'dest' in school_name:
                total_power = 0.0
                for e in spell['enams']:
                    if e['range'] == 'self': continue
                    if e['magic_effect'] in attack_types:
                        #temp += str(e['duration'] * e['mag']) + ' '
                        dur = e['duration']
                        if dur == 0: dur = 1.0
                        total_power += dur  * e['mag']
                avg_dmg_MW = spell['cost'] * 40.0 / 5.0 / 2.0 * 0.66
                s += ' | ' + '%-8s' % ('%0.2f' % total_power)
                s += ' %-8s' % ('%0.2f' % (total_power/avg_dmg_MW))

            res.append(s + '\n')

        if not res: continue
        f = open(os.path.abspath('reports/spellgen/' + idata.get(school, 'schools')), 'w+')
        res = sorted(res, key= lambda x: float(x.split('|')[0].split()[-1]))
        for r in res:
            f.write(r)
        f.close()
    return res

spell_report()
output_names = ['spellmod', 'everything']
outputs.update({'SPEL':new_spells}, output_names)
outputs.update({'SPEL':buffs}, output_names)
outputs.update({'SPEL':bounds}, output_names)

#for s, x in new_spells.iteritems():
    #print s, len(x['SPDT'])


#print attack_types
