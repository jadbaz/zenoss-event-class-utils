import sys
sys.path.append('/home/zenoss/.local/lib/python2.6/site-packages')

# now yaml works
import yaml
import csv
import os.path
import string

FIELD_NAMES = ["class", "rule", "transform", "example"]

infile = sys.argv[1]
basename_file_name = os.path.splitext(infile)[0]
outfile = sys.argv[2] if len(sys.argv) > 2 else basename_file_name + ".csv"

### STRIP NON-PRINTABLE CHARACTERS ####
with open(infile, 'r') as f:
    data = f.read()

# https://stackoverflow.com/questions/8689795/how-can-i-remove-non-ascii-characters-but-leave-periods-and-spaces-using-python/8689826#8689826
printable = set(string.printable)
stripped_data = filter(lambda x: x in printable, data)

with open(infile, "w") as f:
    f.write(stripped_data)
#######################################

with open(infile, 'r') as f:
    contents = yaml.safe_load(f)

mappings = []

for name, evt in contents['event_classes'].iteritems():
    if 'mappings' in evt:
        for event_class_key, mapping in evt['mappings'].iteritems():
            mappings.append({
                "class": name,
                "rule": mapping.get('rule'),
                "transform": mapping.get('transform'),
                "example": mapping.get('example'),
                "explanation": mapping.get("explanation")
            })

    else:
        mappings.append({
            "class": name,
            "rule": None,
            "transform": None,
            "example": None,
            "explanation": None
        })

with open(outfile, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, FIELD_NAMES)
    writer.writerow(dict(zip(writer.fieldnames, writer.fieldnames)))
    for mapping in mappings:
        writer.writerow(mapping)