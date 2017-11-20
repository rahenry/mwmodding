
s = ""
for x in POSITIVE_EFFECT_IDS:
    s += "player->removeeffects " + str(x) + NEWLINE

s += "stopscript " + PREFIX + "script_remove_good_effects" + NEWLINE
