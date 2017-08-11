import mwdata
import index_data

input_files = ["input_data/races"]

raw_data = []
for inp in input_files:
    raw_data += mwdata.read_newline_separated(inp)

print raw_data
