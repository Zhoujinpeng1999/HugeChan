import json

def ParseFromFile(path):
    with open(path, "r") as f:
        return json.loads(f.read())