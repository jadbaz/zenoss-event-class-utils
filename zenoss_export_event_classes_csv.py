import sys
sys.path.append('/home/zenoss/.local/lib/python2.6/site-packages')
sys.path.append('/usr/lib64/python2.6/site-packages')

# now yaml works
import yaml
import csv
import os.path
import string

FIELD_NAMES = ["class", "mapping_id", "rule", "regex", "transform", "example", "explanation"]

infile = sys.argv[1]
basename_file_name = os.path.splitext(infile)[0]
outfile = sys.argv[2] if len(sys.argv) > 2 else basename_file_name + ".csv"
infile_tmp = infile + ".tmp"

### STRIP NON-PRINTABLE CHARACTERS ####
with open(infile, 'r') as f:
    data = f.read()

# https://stackoverflow.com/questions/8689795/how-can-i-remove-non-ascii-characters-but-leave-periods-and-spaces-using-python/8689826#8689826
printable = set(string.printable)
stripped_data = filter(lambda x: x in printable, data)

with open(infile_tmp, "w") as f:
    f.write(stripped_data)
#######################################

with open(infile_tmp, 'r') as f:
    contents = yaml.safe_load(f)

mappings = []

for name, evt in contents['event_classes'].iteritems():
    if 'mappings' in evt:
        for mapping_id, mapping in evt['mappings'].iteritems():
            mappings.append({
                "class": name,
                "mapping_id": mapping_id,
                "rule": mapping.get('rule'),
                "regex": mapping.get('regex'),
                "transform": mapping.get('transform'),
                "example": mapping.get('example'),
                "explanation": mapping.get("explanation")
            })

    else:
        mappings.append({
            "class": name,
            "mapping_id": None,
            "rule": None,
            "regex": None,
            "transform": None,
            "example": None,
            "explanation": None
        })

with open(outfile, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, FIELD_NAMES)
    writer.writerow(dict(zip(writer.fieldnames, writer.fieldnames)))
    for mapping in mappings:
        writer.writerow(mapping)
