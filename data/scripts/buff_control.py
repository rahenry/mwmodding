pcb = PREFIX + "player_current_buffs"
pbp = PREFIX + "player_buff_points"
s = ""
for name, b in spellgen.buffs.iteritems():
    spellid = b['NAME'].replace('_buffeffect', '')
    buffid = b['NAME']
    buff_points = b['buff_points']

    s += ifplayer("getspelleffects", spellid)
    s += doplayer("removespelleffects", spellid)
    s += ifplayer("getspell", buffid)
    s += doplayer("removespell", buffid)
    s += "elseif (" + pcb + "+" + str(buff_points) + ">" + pbp + ")" + NEWLINE
    s += "messagebox YOOOOOO" + NEWLINE
    s += ELSE
    s += doplayer("addspell", buffid)
    s += ENDIF
    s += ENDIF
