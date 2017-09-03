# startscript
# calls buff_dispel when the player casts the special "Dispel Buffs" spell
s = ""
s += ifplayer("getspelleffects", PREFIX + "dispelbuffs")
s += doplayer("removespelleffects", PREFIX + "dispelbuffs")
s += callscript("script_buff_dispel")
s += ENDIF
