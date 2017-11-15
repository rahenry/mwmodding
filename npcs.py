from parameters import *
import utility as ut
import index_data as idata
import esm
import random

import struct
import os
import schema
import outputs
import spellgen
import races
import config

def spell_success_base(skill, will, luck, cost):
    return (skill*2.0 + 0.2*will + 0.1*luck - cost) * 1.25 / 100.

def spell_success(npc, spell):
    worst = 1.0
    for s in spell['schools']:
        succ = spell_success_base(npc[s], npc['willpower'], npc['luck'], spell['cost'])
        if succ < worst: worst = succ
    return worst

def get_tradeflag(x, npc):
    tf = bin(npc['tradeflags'])[2:].zfill(18)
    return tf[-x]

def set_tradeflag(x, val, npc):
    tf = bin(npc['tradeflags'])[2:].zfill(18)
    tf[-x] = str(val)
    npc['tradeflags'] = int(tf, 2)
    



def calc_attributes(npc):
    attribute_coefs = {}
    for attrid in range(8):
        attribute_coefs[attrid] = 0

    for skillid in range(27):
        skillname = idata.get(skillid, 'skills')
        skillattrid = skills[skillname]['attribute']
        base = 5.
        k = 0.1
        if skillid in npc['majors']:
            base = 30.
            k = 1.
            attribute_coefs[skillattrid] += 1.

        elif skillid in npc['minors']:
            base = 15.
            k = 1.
            attribute_coefs[skillattrid] += 0.5
        else:
            attribute_coefs[skillattrid] += 0.2


        skillspec = skills[skillname]['spec']
        classspec = npc['specialisation']
        if (classspec == skillspec):
            base += 5.
            k += 0.5

        if skillname in npc['race_data']:
            base += npc['race_data'][skillname]

        npc[skillname] = math.floor(base + k * (npc['level'] - 1.))
        if npc[skillname] > 100.: npc[skillname] = 100


    for attrid in range(8):
        attrname = idata.get(attrid, 'attributes')
        base = float(npc['race_data'][attrname])
        if attrid == npc['attribute1'] or attrid == npc['attribute2']:
            base += 10.
        npc[attrname] = math.floor(base + attribute_coefs[attrid] * (npc['level'] - 1.))
        if npc[attrname] > 100.: npc[attrname] = 100

    health_mult = 3.0
    if npc['specialisation'] == 0:
        health_mult += 2.
    if npc['specialisation'] == 2:
        health_mult += 1.
    endur_id = idata.get('endurance', 'attributes')
    if npc['attribute1'] == endur_id or npc['attribute2'] == endur_id:
        health_mult += 1.
    npc['health'] = math.floor(0.5 * (npc['strength'] + npc['endurance']) + health_mult * (npc['level'] - 1.))
    npc['spellpts'] = npc['intelligence'] * 2.
    npc['fatigue'] = npc['strength'] + npc['willpower'] + npc['agility'] + npc['endurance']


skills = {}
npcs_base = {}
new_npcs = {}

def process_npcs():
    if not config.options.getboolean('settings', 'process_npcs'): return
    for name, skill in esm.records_original['SKIL'].iteritems():
        skills[name] = dict(skill)
        skills[name].update(schema.decode_subrecord(skills[name]['SKDT'], 'SKDT'))

    last = ""
    for name, npc in esm.records_original['NPC_'].iteritems():
        if 'player' in name: continue
        npcs_base[name] = dict(npc)
        new_npc = npcs_base[name]
        schema.decode_all_subrecords(new_npc)

        #if new_npc['level'] == 7: continue
        #if new_npc['level'] == 17: continue
        #if 'SCRI' in new_npc: print lev
        #print new_npc['level']

        cl = esm.records_original['CLAS'][npc['CNAM'].strip(NULL)]
        new_npc.update(schema.decode_subrecord(cl['CLDT'], 'CLDT'))
        new_npc['majors'] = []
        new_npc['minors'] = []
        for i in range(1,6):
            exec('''new_npc['majors'].append(new_npc['major'+str(i)])''')
            exec('''new_npc['minors'].append(new_npc['minor'+str(i)])''')
        
        race = races.race_data[npc['RNAM'].strip(NULL)]
        new_npc.update(schema.decode_subrecord(race['RADT'], 'RADT'))
        new_npc['race_data'] = {}
        racename = race['FNAM']
        for i in range(1,8):
            exec('''skillid = new_npc['skill'+str(i)]''')
            exec('''skillbonus = new_npc['skillbonus'+str(i)]''')
            skillname = idata.get(skillid, 'skills')
            new_npc['race_data'][skillname] = int(skillbonus)

        new_npc['npcflags'] = struct.unpack('<i', new_npc['FLAG'])[0]

        new_npc['sex'] = 'm'
        if new_npc['npcflags'] % 2 == 1:
            new_npc['sex'] = 'f'

        for i in range(8):
            attr_name = idata.get(i, 'attributes')
            key = attr_name + new_npc['sex']
            exec('''attr_bonus = new_npc[key]''')
            new_npc['race_data'][attr_name] = int(attr_bonus)

        if 'reputation' not in new_npc:
            new_npc['reputation'] = 0


        new_npcs[name] = new_npc

    for name, npc in new_npcs.iteritems():
        calc_attributes(npc)
        a = 0
        for t in schema.scheme_data['NPDT']['scheme']:
            if t not in npc:
                print name, t
                a = 1

        if (a == 1): break
                
        schema.encode_subrecord(npc, 'NPDT')

    new_spell_vendors = {}
    for name, npc in npcs_base.iteritems():
        tradeflags = npc['tradeflags']
        if tradeflags != 0:
            spellmaking = get_tradeflag(12, npc)
            if spellmaking and spellmaking != '0': 
                new_spell_vendors[name] = dict(npc)
                new_spell_vendors[name]['NPCS'] = []

    # give spells to vendors!

    for name, spell in spellgen.new_spells.iteritems():
        attempts = 0
        if 'special' in spell['flags']: continue
        spell['n_occurrences'] = 0
        n_distributed = 0
        while (True):
            n_target = SPELL_MIN_OCCURRENCES
            npc_name = random.choice(new_spell_vendors.keys())
            npc = new_spell_vendors[npc_name]

            if spell['factions'] != []:
                if ut.reductions(npc['ANAM'].strip(NULL)) not in spell['factions']:
                    if random.random() < 1.0: continue # obviously does nothing with this value

            attempts += 1
            if attempts > SPELL_MAX_ATTEMPTS:
                print 'Unable to find vendors for ' + spell['FNAM'] + '; reached ' + str(n_distributed)
                break
            if spell_success(npc, spell) < NPC_VENDOR_CAST_THRESHHOLD: continue
            if npc_name.strip(NULL) in EXCLUDED_NPCS: continue
            if len(npc['NPCS']) < NPC_MAX_SPELLS:
                npc['NPCS'].append(struct.pack('32s', spell['NAME']))
                n_distributed += 1

            if n_distributed >= n_target:
                spell['n_occurrences'] = n_distributed
                break

    for name, npc in new_spell_vendors.iteritems():
        n_spells = len(npc['NPCS'])
        while(True):
            spell_name = random.choice(spellgen.new_spells.keys())
            spell = spellgen.new_spells[spell_name]
            if spell_success(npc, spell) < NPC_VENDOR_CAST_THRESHHOLD: continue
            if 'special' in spell['flags']: break
            if spell['n_occurrences'] > SPELL_MAX_OCCURRENCES: break

            npc['NPCS'].append(spell['NAME'])
            spell['n_occurrences'] += 1



    output_names = ['spellmod', 'everything']
    outputs.update({'NPC_':new_npcs}, output_names)
    outputs.update({'NPC_':new_spell_vendors}, output_names)

    for name, npc in new_spell_vendors.iteritems():
        for s in npc['NPCS']:
            if 'divine' in s:
                #print npc['ANAM']
                1
