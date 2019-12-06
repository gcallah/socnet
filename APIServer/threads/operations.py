import os
import sqlite3
from APIServer.commons.api_utils import read_json, write_json, delete_json

from APIServer.database.sqlite import get_db


def list_threads(path):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM alert")
    return create_alerts(cur.fetchall())


def add_comment(path, thread_id):
	conn = get_db(path)
	cur = conn.cursor()
    return


def get_comments(path, thread_id):
	conn = get_db(path)
	cur = conn.cursor()
	comments = []
    return comments
