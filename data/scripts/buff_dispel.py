# dispel all buffs on the player
s = ""
for name, b in spellgen.buffs.iteritems():
    spellid = b['NAME'].replace('_buffeffect', '')
    buffid = b['NAME']
    buff_points = b['buff_points']
    s += ifplayer("getspell", buffid)
    s += doplayer("removespell", buffid)
    s += ENDIF

s += "stopscript " + PREFIX + "script_buff_dispel" + NEWLINE
