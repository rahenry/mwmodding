import struct
import mwdata
import spellgen

NULL = '\x00'
NEWLINE = struct.pack('b', 13) + '\n'
ENDIF = "endif" + NEWLINE
ELSE = "else" + NEWLINE
PREFIX = "spellmod_"

buffs = {}
for name, s in spellgen.spells.iteritems():
    #print name
    #print s["flags"]
    if "buff" in s["flags"]:
        buff = dict(s)
        buff['NAME'] = [buff['NAME'][0][:-1] + "_buffeffect" + NULL]
        buff['SPDT'] = [struct.pack('<i', 1) + buff['SPDT'][0][4:]]
        buff['spellid'] = [name]
        buffs[name+"_buffeffect"] = buff

spellgen.spells.update(buffs)


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

def s_buff_init():
    s = ""
    for name, b in buffs.iteritems():
        spellid = mwdata.get_subrecord("spellid", b)
        buffid = mwdata.get_subrecord("NAME", b)[0:-1]

        s += ifplayer("getspelleffects", spellid)
        s += doplayer("removespelleffects", spellid)
        s += ifplayer("getspell", buffid)
        s += doplayer("removespell", buffid)
        s += ELSE
        s += doplayer("addspell", buffid)
        s += ENDIF
        s += ENDIF

    return s

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

script_list = {"s_buff_init" : s_buff_init}
scripts = {}
for name, f in script_list.iteritems():
    script = make_script(name, f)
    scripts[name] = pack_script(script, name)

print scripts

