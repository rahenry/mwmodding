import colour
import subprocess
import os

if not (os.path.exists("icons")):
    os.makedirs("icons")

blackness_threshhold = 0.15
def get_hsl_average(file_name):
    command = ['convert', file_name, 'txt:']
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)

    a = []
    for l in proc.stdout.readlines()[1:]:
        x = map(lambda x: int(x)/255., ((l.split()[1]).strip('(')).strip(')').split(','))
        c = colour.Color(rgb=(x[0], x[1], x[2]))
        if (c.hsl[2] > blackness_threshhold):
            a.append(c)

    hsl_average = (0, 0, 0)
    for x in a:
        hsl_average = tuple(map(sum, zip(hsl_average, x.hsl)))

    return map(lambda x: x/float(len(a)), hsl_average)

def recolour(source_file, objective_file, output_file):
    print source_file, objective_file, output_file
    h1 = get_hsl_average(source_file)[0]
    h2 = get_hsl_average(objective_file)[0]
    s1 = get_hsl_average(source_file)[1]
    s2 = get_hsl_average(objective_file)[1]
    l1 = get_hsl_average(source_file)[2]
    l2 = get_hsl_average(objective_file)[2]

    hue_argument = ((h2-h1) * 200) + 100
    saturation_argument = ((s2/s1) * 100.)
    lightness_argument = ((l2/l1) * 100.)
    command = ['convert', source_file, '-modulate', str(lightness_argument)+','+str(saturation_argument)+','+str(hue_argument), output_file]
    proc = subprocess.call(command)

    #command = ['convert', source_file, objective_file, output_file, '+append', 'test.jpg']
    proc = subprocess.call(command)


    #proc = subprocess.call(['mirage', 'test.jpg'])
