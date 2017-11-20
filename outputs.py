import os 
import esm
import config
output_names = [config.options.get('settings', 'output_path')]
outputs = {}
def make_output(name):
    outputs[name] = {}
    outputs[name]['path'] = os.path.abspath(o)
    outputs[name]['data'] = {}

for o in output_names:
    outputs[o] = {}
    outputs[o]['path'] = os.path.abspath(o)
    outputs[o]['data'] = {}
    make_output(o)

def write():
    for name, output in outputs.iteritems():
        esm.write_esp(output['data'], output['path'])

def update(recs, targets):
    if output_names[0] not in targets:
        targets.append(output_names[0])
    for o in targets:
        if o not in output_names:
            make_output(o)
        for rtype in recs:
            if not rtype in outputs[o]['data']:
                outputs[o]['data'][rtype] = {}
            outputs[o]['data'][rtype].update(recs[rtype])
