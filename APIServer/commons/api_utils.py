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


def write_json(path, id, content):

    jfile = open(path, 'r')
    feeds = json.load(jfile)
    feeds[id] = content
    jfile.close()

    jfile = open(path, 'w')
    json.dump(feeds, jfile)
    jfile.close()


def delete_json(path, id):

    jfile = open(path, 'r')
    feeds = json.load(jfile)
    jfile.close()

    del feeds[id]

    jfile = open(path, 'w')
    json.dump(feeds, jfile)
    jfile.close()
