import json

def json_savefile(jsondata, filename):
    with open(filename, 'w') as output_file:
        json.dump(jsondata, output_file, indent=4)
        
def hash_json(jsondata):
    return frozenset((str(x), str(y)) for x, y in jsondata.items())