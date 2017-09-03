from parameters import *
import utility as ut
import index_data as idata
import esm
import random

import struct
import os
import schema
import outputs
import spellgen


race_data = {}
for name, race in esm.records_original['RACE'].iteritems():
    race_data[name] = dict(race)
    race.update(schema.decode_subrecord(race['RADT'], 'RADT'))

