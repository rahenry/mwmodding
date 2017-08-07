import struct 
from index_data import *
from mwdata import *
from colour_converter import *
from magic_effects import *

NULL = '\x00'

f = open("test", "w+")
f.write(encode_record('MGEF', records['MGEF'][0]))
f.close()

#recolour("colour_test/1.txt", "colour_test/2.txt", "test1.jpg")


