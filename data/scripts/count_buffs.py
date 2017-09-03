# startscript

pcb = PREFIX + "player_current_buffs"
pbp = PREFIX + "player_buff_points"
s = ""
s += setvar(pcb, str(0))
for name, b in spellgen.buffs.iteritems():
    spellid = b['NAME'].replace('_buffeffect', '')
    buffid = b['NAME']
    buff_points = b['buff_points']

    s += ifplayer("getspell", buffid)
    s += setvar(pcb, pcb + "+" + str(buff_points))
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
s += callscript("script_buff_dispel")
s += messagebox("Your magickal auras collapse!")
s += ENDIF
