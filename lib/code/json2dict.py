import json

def json2dict(json_str):
    return json.loads(json_str)

def dict2json(dict):
    return json.dumps(dict)