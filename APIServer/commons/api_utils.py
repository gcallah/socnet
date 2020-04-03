import json
ERROR = "Error"


def err_return(s):
    return {ERROR: s}


def read_json(path):
    try:
        with open(path, 'r') as jfile:
            json_file = json.load(jfile)
        return json_file
    except FileNotFoundError:
        try:
            with open('APIServer/' + path, 'r') as jfile:
                json_file = json.load(jfile)
            return json_file
        except FileNotFoundError:
            return err_return("Json file not found")
        except json.decoder.JSONDecodeError:
            return err_return("Not a valid json file")
    except json.decoder.JSONDecodeError:
        return err_return("Not a valid json file")
