import os 
import esm
output_names = ['spellmod', 'everything']
outputs = {}
for o in output_names:
    outputs[o] = {}
    outputs[o]['path'] = os.path.abspath('output/'+o+'.esp')
    outputs[o]['data'] = {}

def write():
    for name, output in outputs.iteritems():
        esm.write_esp(output['data'], output['path'])

def update(recs, output_names):
    for o in output_names:
        for rtype in recs:
            if not rtype in outputs[o]['data']:
                outputs[o]['data'][rtype] = {}
            outputs[o]['data'][rtype].update(recs[rtype])
