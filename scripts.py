import struct
import spellgen
import esm
import os
import utility as ut
import outputs
from parameters import *

NULL = '\x00'
NEWLINE = struct.pack('b', 13) + '\n'
ENDIF = "endif" + NEWLINE
ELSE = "else" + NEWLINE
ELSEIF = "elseif" + NEWLINE
BUFF_INT_WEIGHT = 3.0
BUFF_WILL_WEIGHT = 2.0
BUFF_PERS_WEIGHT = 5.0
BUFF_LUCK_WEIGHT = 0.5
BUFFS_AT_100 = 5.0
ALCH_COOLDOWN = 30
BOUND_COOLDOWN = 60
POSITIVE_EFFECT_IDS = [40,64,65,66,8,4,117,79,82,80,84,83,81,6,9,10,41,43,68,95,94,96,90,91,93,98,99,97,92,74,77,75,78,76,42,3,11,67,1,59,0,2]

new_scripts = {}
new_startscripts = {}

def ifplayer(func, arg):
    return "if player->" + func + ''' "''' + arg + '''"''' + " == 1" + NEWLINE

def doplayer(func, arg):
    return "player->" + func + ''' "''' + arg + '''"''' + NEWLINE

def startscript(name):
    return "begin " + name + NEWLINE

def endscript(name):
    return "end " + name

def callscript(name):
    return "startscript " + PREFIX + name + NEWLINE

def setvar(var, arg):
    return "set " + var + " to " + arg + NEWLINE

def messagebox(stuff):
    return '''messagebox "''' + stuff + '"' + NEWLINE

def pack_script(script, name):
    res = {}
    SCHD = ""
    SCHD += struct.pack("<32s", name)
    SCHD += struct.pack("<i", 0)
    SCHD += struct.pack("<i", 0)
    SCHD += struct.pack("<i", 0)
    SCHD += struct.pack("<i", 0)
    SCHD += struct.pack("<i", 0)
    res["SCHD"] = [SCHD]
    res["SCVR"] = [""]
    res["SCDT"] = [""]
    res["SCTX"] = [script]
    return res

esm.record_subrecord_orderings['SSCR'] = ['NAME', 'DATA']
def make_startscript(script_name):
    res = {}
    res['NAME'] = script_name
    res['DATA'] = NULL
    new_startscripts[script_name] = res

def make_script(script_file):
    f = open(script_file)
    script_body = ''
    script_name = PREFIX + 'script_' + os.path.basename(script_file).replace('.py', '')

    if 'count_telvanni' in script_name:
        script_name = 'CountWizardSpells'

    comments = []
    for l in f.readlines():
        if l[0] == '#': comments.append(l)
        else: script_body += l

    for c in comments:
        if 'startscript' in c:
            make_startscript(script_name)

    exec(script_body)
    s = startscript(script_name) + s + endscript(script_name)
    new_scripts[script_name] = pack_script(s, script_name)

script_dir = os.path.abspath('data/scripts')
sfiles = ut.get_file_list(script_dir)
for s in sfiles:
    make_script(s)

globdata = {
        "player_current_buffs" : ('l', 0),
        "player_buff_points" : ('l', 5),
        }

globs = {}
for glob, info in globdata.iteritems():
    res = {}
    res['NAME'] = [PREFIX + glob + NULL]
    res['FNAM'] = [struct.pack('c', info[0])]
    res['FLTV'] = [struct.pack('<i', info[1])]
    globs[PREFIX + glob] = res

output_names = ['everything', 'spellmod']
outputs.update({'SCPT':new_scripts}, output_names)
outputs.update({'GLOB':globs}, output_names)
outputs.update({'SSCR':new_startscripts}, output_names)
