import sqlite3

def get_sqlite_path(path):
    return path + '.db'


def get_db(path):
    sqlite_path = get_sqlite_path(path)
    return sqlite3.connect(sqlite_path)


def sqlite_init(path, schema):
    db = get_db(path)
    with open(schema) as f:
        db.executescript(f.read())
