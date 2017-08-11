import struct
import mwdata
import spellgen

NULL = '\x00'
NEWLINE = struct.pack('b', 13) + '\n'
buffs = {}
for name, s in spellgen.spells.iteritems():
    if "buff" in s["flags"]:
        buff = dict(s)
        buff['NAME'] = [buff['NAME'][0][:-1] + "_buffeffect" + NULL]
        buff['SPDT'] = [struct.pack('<i', 1) + buff['SPDT'][0][4:]]
        buff['spellid'] = [name]
        buffs[name+"_buffeffect"] = buff

spellgen.spells.update(buffs)

script1 = ""
script1 += "begin script1" + NEWLINE

for name, b in buffs.iteritems():
    s = {}
    script1 += "if player->getspelleffects " + mwdata.get_subrecord("spellid", b) + " == 1" + NEWLINE
    script1 += "player->removespelleffects " + mwdata.get_subrecord("spellid", b) + NEWLINE

    script1 += "if player->getspell " + mwdata.get_subrecord("NAME", b)[0:-1] + " == 1" + NEWLINE
    script1 += "player->removespell " + mwdata.get_subrecord("NAME", b)[0:-1] + NEWLINE
    script1 += "elseif player->getspell " + mwdata.get_subrecord("NAME", b)[0:-1] + " == 0" + NEWLINE
    script1 += "player->addspell " + mwdata.get_subrecord("NAME", b)[0:-1] + NEWLINE
    script1 += "endif" + NEWLINE

    script1 += "endif" + NEWLINE

script1 += "end script1"

scripts = {}
scripts["script1"] = {}
SCHD = ""
SCHD += struct.pack("<32s", "script1")
SCHD += struct.pack("<i", 0)
SCHD += struct.pack("<i", 0)
SCHD += struct.pack("<i", 0)
SCHD += struct.pack("<i", 0)
SCHD += struct.pack("<i", 0)
scripts["script1"]["SCHD"] = [SCHD]
scripts["script1"]["SCVR"] = [""]
scripts["script1"]["SCDT"] = [""]
scripts["script1"]["SCTX"] = [script1]

    


f = open("chartest", 'w+')
for i in range(25):
    f.write(struct.pack('b', 13))
