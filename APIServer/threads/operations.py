import os
import sqlite3

from APIServer.database.sqlite import get_db
from APIServer import db
from APIServer.database.models import Thread,Comment

def add_comment(comment, thread_id):
    fetched_thread = Thread.query.get(thread_id)
    if fetched_thread is None:
        return {'message' : 'Thread ' + str(thread_id) + ' does not exist'}, 404
    first_comment_id = fetched_thread.first_comment_id
    last_comment_id = fetched_thread.last_comment_id
    # add the new comment to the commnet table
    comment_text = comment['text']
    new_comment = Comment(content=comment_text)
    db.session.add(new_comment)
    db.session.commit()
    # update the first and last comment id in thread table
    new_id = new_comment.id
    fetched_thread.last_comment_id = new_id
    if first_comment_id == -1:
        fetched_thread.first_comment_id = new_id
    # update last comment to point to the new comment
    if last_comment_id != -1:
        fetched_comment = Comment.query.get(last_comment_id)
        fetched_comment.next_comment_id = new_id
    db.session.commit()
    return 'Comment %d inserted to thread %d' % (new_id, thread_id)


def get_comments(thread_id):
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

def delete_thread(thread_id):
    """
    delete all comments and thread for the given thread id
    """
    fetched_thread = Thread.query.get(thread_id)
    if fetched_thread is None:
        return {'message' : 'Thread ' + str(thread_id) + ' does not exist'}, 404
    first_comment_id = fetched_thread.first_comment_id
    # delete all associated comments
    comment_id = first_comment_id
    while comment_id != -1:
        fetched_comment = Comment.query.get(comment_id)
        comment_id = fetched_comment.next_comment_id
        db.session.delete(fetched_comment)
    # delete the thread from thread table
    db.session.delete(fetched_thread)
    db.session.commit()
    return 'Deleted thread %d' % (thread_id)