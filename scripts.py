import struct
import spellgen
import esm

NULL = '\x00'
NEWLINE = struct.pack('b', 13) + '\n'
ENDIF = "endif" + NEWLINE
ELSE = "else" + NEWLINE
ELSEIF = "elseif" + NEWLINE
PREFIX = "spellmod_"
BUFF_INT_WEIGHT = 3.0
BUFF_WILL_WEIGHT = 2.0
BUFF_PERS_WEIGHT = 5.0
BUFF_LUCK_WEIGHT = 0.5
BUFFS_AT_100 = 5.0
ALCH_COOLDOWN = 30
BOUND_COOLDOWN = 60
POSITIVE_EFFECT_IDS = [40,64,65,66,8,4,117,79,82,80,84,83,81,6,9,10,41,43,68,95,94,96,90,91,93,98,99,97,92,74,77,75,78,76,42,3,11,67,1,59,0,2]

buffs = {}
bound_effects = {}
for name, s in spellgen.new_spells.iteritems():
    if "buff" in s["flags"] or "bound" in s['flags']:
        buff = dict(s)
        buff['NAME'] = [buff['NAME'][0][:-1] + "_buffeffect" + NULL]
        buff['SPDT'] = [struct.pack('<i', 1) + buff['SPDT'][0][4:]]
        buff['spellid'] = [name]
        buff['flags'] = []
        if "buff" in s["flags"]:
            buffs[name+"_buffeffect"] = buff
        else:
            bound_effects[name+"_buffeffect"] = buff

spellgen.new_spells.update(buffs)
spellgen.new_spells.update(bound_effects)


def ifplayer(func, arg):
    return "if player->" + func + ''' "''' + arg + '''"''' + " == 1" + NEWLINE

def doplayer(func, arg):
    return "player->" + func + ''' "''' + arg + '''"''' + NEWLINE

def startscript(name):
    return "begin " + name + NEWLINE

def endscript(name):
    return "end " + name

def make_script(name, func):
    return startscript(name) + func() + endscript(name)

def callscript(name):
    return "startscript " + PREFIX + name + NEWLINE

def setvar(var, arg):
    return "set " + var + " to " + arg + NEWLINE

def messagebox(stuff):
    return '''messagebox "''' + stuff + '"' + NEWLINE

def pack_script(script, name):
    res = {}
    SCHD = ""
    SCHD += struct.pack("<32s", name)
    SCHD += struct.pack("<i", 0)
    SCHD += struct.pack("<i", 0)
    SCHD += struct.pack("<i", 0)
    SCHD += struct.pack("<i", 0)
    SCHD += struct.pack("<i", 0)
    res["SCHD"] = [SCHD]
    res["SCVR"] = [""]
    res["SCDT"] = [""]
    res["SCTX"] = [script]
    return res

def s_buff_init():
    pcb = PREFIX + "player_current_buffs"
    pbp = PREFIX + "player_buff_points"
    s = ""
    for name, b in buffs.iteritems():
        spellid = b['NAME']
        buffid = b['NAME']
        buffpoints = b['buffpoints']

        s += ifplayer("getspelleffects", spellid)
        s += doplayer("removespelleffects", spellid)
        s += ifplayer("getspell", buffid)
        s += doplayer("removespell", buffid)
        s += "elseif (" + pcb + "+" + str(buffpoints) + ">" + pbp + ")" + NEWLINE
        s += "messagebox YOOOOOO" + NEWLINE
        s += ELSE
        s += doplayer("addspell", buffid)
        s += ENDIF
        s += ENDIF

    return s

def s_buff_dispel():
    # dispel all buffs on the player
    s = ""
    for name, b in buffs.iteritems():
        spellid = b['NAME']
        buffid = b['NAME']
        s += ifplayer("getspell", buffid)
        s += doplayer("removespell", buffid)
        s += ENDIF

    s += "stopscript " + PREFIX + "s_buff_dispel" + NEWLINE
    return s

def s_catch_buff_dispel():
    # calls buff_dispel when the player casts the special "Dispel Buffs" spell
    s = ""
    s += ifplayer("getspelleffects", PREFIX + "dispel buffs")
    s += doplayer("removespelleffects", PREFIX + "dispel buffs")
    s += callscript("s_buff_dispel")
    s += ENDIF
    return s

def s_count_buffs():
    pcb = PREFIX + "player_current_buffs"
    pbp = PREFIX + "player_buff_points"
    s = ""
    s += setvar(pcb, str(0))
    for name, b in buffs.iteritems():
        spellid = b['NAME']
        buffid = b['NAME']
        buffpoints = b['buffpoints']

        s += ifplayer("getspell", buffid)
        s += setvar(pcb, pcb + "+" + str(buffpoints))
        s += ENDIF

    total = (BUFF_INT_WEIGHT + BUFF_WILL_WEIGHT + BUFF_PERS_WEIGHT + BUFF_LUCK_WEIGHT) * 100.0
    r = (BUFFS_AT_100-1.0) / total
    wint = BUFF_INT_WEIGHT * r
    wwill = BUFF_WILL_WEIGHT * r
    wpers = BUFF_PERS_WEIGHT * r
    wluck = BUFF_LUCK_WEIGHT * r


    x = "player->getintelligence * " + str(wint) + " + player->getwillpower * " + str(wwill) + " + player->getpersonality * " + str(wpers) + " + player->getluck * " + str(wluck) + " + 1"
    s += setvar(pbp, x)
    s += "if " + pcb + " > " + pbp + NEWLINE
    s += callscript("s_buff_dispel")
    s += messagebox("Your magickal auras collapse!")
    s += ENDIF

    return s

def s_removepositiveeffects():
    s = ""
    for x in POSITIVE_EFFECT_IDS:
        s += "player->removeeffects " + str(x) + NEWLINE

    s += "stopscript " + PREFIX + "s_removepositiveeffects" + NEWLINE
    return s

def s_bound_items():
    s = ""
    s += "float cooldown" + NEWLINE
    s += "float duration" + NEWLINE
    s += setvar("cooldown", "cooldown - getsecondspassed")
    s += setvar("duration", "duration - getsecondspassed")
    s += "if cooldown >= 0" + NEWLINE
    s += doplayer("addspell", PREFIX+"Bound Cooldown")
    for name, spell in spellgen.new_spells.iteritems():
        if 'bound' in spell['flags']:
            s += ifplayer("getspelleffects", name)
            s += '''messagebox "You can't use another bound for %.0fs!" cooldown''' + NEWLINE
            s += doplayer("removespelleffects", name)
            s += ENDIF
    s += ELSE
    s += doplayer("removespell", PREFIX+"Bound Cooldown")
    for name, spell in spellgen.new_spells.iteritems():
        if 'bound' in spell['flags']:
            buffid = name.strip(NULL) + "_buffeffect"
            s += ifplayer("getspelleffects", name)
            s += doplayer("removespelleffects", name)
            s += doplayer("addspell", buffid)
            s += setvar("cooldown", str(BOUND_COOLDOWN))
            s += setvar("duration", str(spell['duration']))
            s += ENDIF
    s += ENDIF
    s += "if duration < 0" + NEWLINE
    for name, spell in spellgen.new_spells.iteritems():
        if 'bound' in spell['flags']:
            buffid = name.strip(NULL) + "_buffeffect"
            s += doplayer("removespell", buffid)
    s += ENDIF
    return s

def s_alch_cooldown():
    s = ""
    s += "float cooldown" + NEWLINE
    s += "float trigger" + NEWLINE
    s += setvar("cooldown", "cooldown - getsecondspassed")
    s += setvar("trigger", "trigger - getsecondspassed")
    s += "if cooldown < 0" + NEWLINE
    s += doplayer("removespell", PREFIX+"Alchemy Cooldown")
    s += ENDIF
    s += "if trigger > 0" + NEWLINE
    s += "return" + NEWLINE
    s += ENDIF


    s += ifplayer("getsoundplaying", "drink")
    s += setvar("trigger", "0.8")

    s += "if (cooldown > 0)" + NEWLINE
    s += callscript("s_removepositiveeffects")
    s += "return" + NEWLINE
    s += ENDIF

    s += setvar("cooldown", str(ALCH_COOLDOWN))
    s += doplayer("addspell", PREFIX+"Alchemy Cooldown")
    s += ENDIF
    return s


def s_main():
    return s_count_buffs() + s_catch_buff_dispel() + s_buff_init()

script_list = {
    "s_buff_init" : s_buff_init,
    "s_buff_dispel" : s_buff_dispel,
    "s_catch_buff_dispel" : s_catch_buff_dispel,
    "s_count_buffs" : s_count_buffs,
    "s_alch_cooldown" : s_alch_cooldown,
    "s_removepositiveeffects" : s_removepositiveeffects,
    "s_bound_items" : s_bound_items,
    }

start_script_list = [
        "s_buff_init",
        "s_catch_buff_dispel",
        "s_count_buffs",
        "s_alch_cooldown",
        "s_bound_items",
        ]

globdata = {
        "player_current_buffs" : ('l', 0),
        "player_buff_points" : ('l', 5),
        }

scripts = {}
for name, f in script_list.iteritems():
    name = PREFIX + name
    script = make_script(name, f)
    scripts[name] = pack_script(script, name)

start_scripts = {}
esm.record_subrecord_orderings['SSCR'] = ['NAME', 'DATA']
for s in start_script_list:
    res = {}
    res['NAME'] = [PREFIX + s + NULL]
    res['DATA'] = [NULL]
    start_scripts[PREFIX + s] = res

globs = {}

for glob, info in globdata.iteritems():
    res = {}
    res['NAME'] = [PREFIX + glob + NULL]
    res['FNAM'] = [struct.pack('c', info[0])]
    res['FLTV'] = [struct.pack('<i', 0)]
    globs[PREFIX + glob] = res

