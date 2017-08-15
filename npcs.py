import mwdata
import spellgen
import struct
import random
import magic_effects
import index_data

NPC_MAX_SPELLS = 10
NPC_MIN_SPELLS = 5
CAN_CAST_THRESHHOLD = 0.5

def populate_npcs(records, spells):
    spellmaking_npcs = {}
    for ident, npc in records['NPC_'].iteritems():
        if (ident != 'player\x00'):
            aiflags = npc['AIDT'][0][8:]
            f = mwdata.unpack_flags(aiflags)
            if f[-12] == 1:
                new_id = ident.split()[0].lower()
                spellmaking_npcs[new_id] = process_npc(npc, spells)
    for ident, npc  in spellmaking_npcs.iteritems():
        continue
        #print "..."
        #print ident
        #print npc
        #print npc['spell_keys']
        1
    return spellmaking_npcs

def get_random_spell(spell_keys):
    while (True):
        new_spell_key = random.choice(spell_keys)
        if ("buffeffect" in new_spell_key): continue
        return new_spell_key

def process_npc(npc, spells):
    npc['NPCS'] = []
    npc['spell_keys'] = []
    spell_keys = []
    for k in spells.iterkeys():
        if "special" in spells[k]['flags']: continue
        if spells[k]['type'] == 0:
            spell_keys.append(k)
    n_spells = 0
    attempts = 0
    max_attempts = 100
    while (n_spells < NPC_MAX_SPELLS): 
        if (attempts > max_attempts): break
        attempts += 1
        new_spell_key = get_random_spell(spell_keys)
        if new_spell_key not in npc['spell_keys'] and can_cast_spell(npc, spells[new_spell_key]):
            npc['NPCS'].append(struct.pack('<32s', new_spell_key))
            npc['spell_keys'].append(new_spell_key)
            n_spells += 1
    return npc

def success_formula(skill, cost, will, luck):
    return 0.01*1.25 * (2.0 * skill + 0.2*will + 0.1*luck - cost)

def get_attr(npdt, attr_id):
    if (len(npdt) == 12):
        return 80
    else:
        return struct.unpack('<b', npdt[attr_id])[0]

def get_skill(npdt, skill_id):
    if (len(npdt) == 12):
        #print mwdata.get_subrecord('FNAM', npc)
        # autocalced npcs - there are only three of them!
        return 80
    else:
        return struct.unpack('<b', npdt[10:37][skill_id])[0]

def can_cast_spell(npc, spell):
    worst_skill = 100
    npdt = mwdata.get_subrecord('NPDT', npc)
    for s in spell['schools']:
        sname = index_data.get_key(s, 'schools')
        skillid = index_data.get_index(sname, 'skills')
        skill = get_skill(npdt, skillid)
        if (skill < worst_skill): worst_skill = skill

    will = get_attr(npdt, index_data.get_index("willpower", "attributes"))
    luck = get_attr(npdt, index_data.get_index("luck", "attributes"))
    success = success_formula(worst_skill, spell['cost'], will, luck)
    #if ("arrille" in mwdata.get_subrecord('NAME', npc)):
        #print 'hey'
        #info = (npc['FNAM'][0], spell['FNAM'][0], worst_skill, success)
        #print info
    return (success > CAN_CAST_THRESHHOLD)
        #npc['NPCS'].append(struct.pack('<32s', mwdata.get_subrecord('NAME', spell)[:-1]))
    #print skills_raw
