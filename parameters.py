import os 
import math

RECORD_TYPES_OF_INTEREST = ['TES3', 'MGEF', 'SPEL', 'SCPT', 'RACE', 'NPC_', 'GLOB', 'ARMO', 'WEAP', 'ENCH', 'CLAS', 'RACE', 'SKIL']

# distributing spells to npcs
NPC_MIN_SPELLS = 8
NPC_MAX_SPELLS = 15
SPELL_MIN_OCCURRENCES = 3
SPELL_MAX_OCCURRENCES = 10
EXCLUDED_NPCS = ['todd', 'used clutter salesman']



# spellgen
SPELL_ATTACK_BASE_COST = 4.0 / 10.0
DE_3 = 1.13
DE_10 = 1.30
DURATION_EFFICIENCY_FACTOR = 100.0
DURATION_EFFICIENCY_COEF = 1.2 / math.log(3.0 * DURATION_EFFICIENCY_FACTOR)
DURATION_EFFICIENCY_FACTOR = pow(pow(3.0, DE_3) / pow(10.0, DE_10), 1.0 / (DE_3 - DE_10))
DURATION_EFFICIENCY_COEF = DE_3 / math.log(3.0 * DURATION_EFFICIENCY_FACTOR)

area_efficiency_pts = (
        (10, 0.88),
        (50, 0.4))
aep = area_efficiency_pts
AREA_EFFICIENCY_POWER = math.log(aep[1][1]/aep[0][1], (aep[0][0]+1.)/(aep[1][0]+1.))
AREA_EFFICIENCY_COEF = aep[0][1] * pow(aep[0][0], AREA_EFFICIENCY_POWER)
AREA_EFFICIENCIES = {
        0 : 1.0,
        1: 1.0,
        2: 1.0,
        3: 0.98,
        4: 0.95,
        5: 0.92,
        }

#AREA_EFFICIENCY_FACTOR = -0.2*math.log(0.75)

NULL = '\x00'
PREFIX = 'kuju_'
TEST1 = 5
REDUCTIONS = [
        lambda x: x.replace('_', ''),
        lambda x: x.replace(' ', ''),
        lambda x: x.lower(),
        ]
MW_DATA_PATH = os.path.abspath(os.path.expanduser('~/.local/share/openmw/data'))
AUTHOR_NAME = 'kuju'
MOD_DESCRIPTION = 'mod123'
DATA_DIR = os.path.abspath('data')

# spellgen
INSTANCES_MIN_BASE = 5
INSTANCES_MAX_BASE = 1000
SDEV_EFFICIENCY_MAX = 1.1
SUCCESS_THRESHHOLD = 0.5

# npcs
# spells
NPC_CAST_THRESHHOLD = 0.9
NPC_SELL_CAST_THRESHHOLD = 0.4
