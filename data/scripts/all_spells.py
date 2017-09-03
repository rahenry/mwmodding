s = ''
for name, b in spellgen.new_spells.iteritems():
    spellid = b['NAME']
    s += doplayer("addspell", spellid)
