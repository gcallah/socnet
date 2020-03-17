import json
ERROR = "Error:"


def err_return(s):
    return {ERROR: s}


def read_json(path):
    try:
        with open(path, 'r') as jfile:
            json_file = json.load(jfile)
        return json_file
    except FileNotFoundError:
        return err_return("Json file not found")
