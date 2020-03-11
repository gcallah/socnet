import os
import sqlite3

from APIServer.database.sqlite import get_db
from APIServer import db
from APIServer.database.models import Thread,Comment

def add_comment_beta(comment, thread_id):
    fetched_thread = Thread.query.get(thread_id)
    if fetched_thread is None:
        return {'message' : 'Thread ' + str(thread_id) + ' does not exist'}, 404
    first_comment_id = fetched_thread.first_comment_id
    last_comment_id = fetched_thread.last_comment_id
    comment_text = comment['text']
    new_comment = Comment(content=comment_text)
    db.session.add(new_comment)
    db.session.commit()

    new_id = new_comment.id
    fetched_thread.last_comment_id = new_id
    if first_comment_id == -1:
        fetched_thread.first_comment_id = new_id
    if last_comment_id != -1:
        fetched_comment = Comment.query.get(last_comment_id)
        fetched_comment.next_comment_id = new_id
    db.session.commit()
    return 'Comment %d inserted to thread %d' % (new_id, thread_id)


def get_comments_beta(thread_id):
    fetched_thread = Thread.query.get(thread_id)
    if fetched_thread is None:
        return {'message' : 'Thread ' + str(thread_id) + ' does not exist'}, 404
    first_comment_id = fetched_thread.first_comment_id
    comment_id = first_comment_id
    comments = []
    while comment_id != -1:
        fetched_comment = Comment.query.get(comment_id)
        comments.append({comment_id: fetched_comment.content})
        comment_id = fetched_comment.next_comment_id
    return comments


def add_comment(path, comment, thread_id):
    conn = get_db(path)
    cur = conn.cursor()

    cur.execute('SELECT first_comment_id, last_comment_id FROM thread WHERE id = \'%d\'' % (thread_id))
    thread_info = cur.fetchone()
    if thread_info is None:
        return {'message' : 'Thread ' + str(thread_id) + ' does not exist'}, 404

    first_comment_id = thread_info[0]
    last_comment_id = thread_info[1]

    comment_text = comment['text']

    columns = '(content, next_comment_id)'
    values = '(\'%s\', \'-1\')' % (comment_text)
    cur.execute("INSERT INTO comment " + columns +" VALUES " + values)
    new_comment_id = cur.lastrowid

    cur.execute('UPDATE thread SET last_comment_id = \'%d\' WHERE id = \'%d\'' % (new_comment_id, thread_id))
    if first_comment_id == -1:
        cur.execute('UPDATE thread SET first_comment_id = \'%d\' WHERE id = \'%d\'' % (new_comment_id, thread_id))

    if last_comment_id != -1:
        cur.execute('UPDATE comment SET next_comment_id = \'%d\' WHERE id = \'%d\'' % (new_comment_id, last_comment_id))

    conn.commit()
    conn.close()
    return 'Comment %d inserted to thread %d' % (new_comment_id, thread_id)


def get_comments(path, thread_id):
    conn = get_db(path)
    cur = conn.cursor()
    comments = []

    cur.execute('SELECT first_comment_id FROM thread WHERE id = \'%d\'' % (thread_id))

    result = cur.fetchone()
    if result is None:
        return {'message' : 'Thread ' + str(thread_id) + ' does not exist'}, 404

    comment_id = result[0]
    while True:
        if comment_id == -1:
            break
        cur.execute('SELECT content, next_comment_id FROM comment WHERE id = \'%d\'' % (comment_id))
        result = cur.fetchone()
        comment_text = result[0]
        next_comment_id = result[1]
        comment = {comment_id: comment_text}
        comments.append(comment)
        comment_id = next_comment_id
    conn.close()
    return comments
