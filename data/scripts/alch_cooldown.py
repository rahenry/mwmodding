# startscript
s = ""
s += "float cooldown" + NEWLINE
s += "float trigger" + NEWLINE
s += setvar("cooldown", "cooldown - getsecondspassed")
s += setvar("trigger", "trigger - getsecondspassed")
s += "if cooldown < 0" + NEWLINE
s += doplayer("removespell", PREFIX+"alchemycooldown")
s += ENDIF
s += "if trigger > 0" + NEWLINE
s += "return" + NEWLINE
s += ENDIF


s += ifplayer("getsoundplaying", "drink")
s += setvar("trigger", "0.8")

s += "if (cooldown > 0)" + NEWLINE
s += callscript("script_remove_good_effects")
s += "return" + NEWLINE
s += ENDIF

s += setvar("cooldown", str(ALCH_COOLDOWN))
s += doplayer("addspell", PREFIX+"alchemycooldown")
s += ENDIF
