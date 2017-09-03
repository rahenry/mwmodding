# startscript
s = ""
s += "float cooldown" + NEWLINE
s += "float duration" + NEWLINE
s += setvar("cooldown", "cooldown - getsecondspassed")
s += setvar("duration", "duration - getsecondspassed")
s += "if cooldown >= 0" + NEWLINE
s += doplayer("addspell", PREFIX+"boundcooldown")
for name, spell in spellgen.new_spells.iteritems():
    if 'bound' in spell['flags']:
        s += ifplayer("getspelleffects", name)
        s += '''messagebox "You can't conjure another item for %.0fs!" cooldown''' + NEWLINE
        s += doplayer("removespelleffects", name)
        s += ENDIF
s += ELSE
s += doplayer("removespell", PREFIX+"boundcooldown")
for name, spell in spellgen.new_spells.iteritems():
    if 'bound' in spell['flags']:
        buffid = name.strip(NULL) + "_boundeffect"
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
        buffid = name.strip(NULL) + "_boundeffect"
        s += doplayer("removespell", buffid)
s += ENDIF

