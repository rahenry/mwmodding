s = ""
s += "float cooldown" + NEWLINE
s += "float duration" + NEWLINE
s += setvar("cooldown", "cooldown - getsecondspassed")
s += setvar("duration", "duration - getsecondspassed")
s += "if cooldown >= 0" + NEWLINE
s += doplayer("addspell", PREFIX+"Bound Cooldown")
for name, spell in spellgen.spells.iteritems():
    if 'bound' in spell['flags']:
        s += ifplayer("getspelleffects", name)
        s += '''messagebox "You can't use another bound for %.0fs!" cooldown''' + NEWLINE
        s += doplayer("removespelleffects", name)
        s += ENDIF
s += ELSE
s += doplayer("removespell", PREFIX+"Bound Cooldown")
for name, spell in spellgen.spells.iteritems():
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
for name, spell in spellgen.spells.iteritems():
    if 'bound' in spell['flags']:
        buffid = name.strip(NULL) + "_buffeffect"
        s += doplayer("removespell", buffid)
s += ENDIF

