CREATE TABLE IF NOT EXISTS alert (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_datetime TEXT,
    event_zipcode TEXT,
    event_city TEXT,
    event_state TEXT,
    event_country TEXT,
    event_type TEXT,
    event_description TEXT,
    event_severity TEXT,
    msg_sender TEXT
);
CREATE TABLE IF NOT EXISTS thread (
    id INTEGER PRIMARY KEY,
    first_comment_id INTEGER,
    last_comment_id INTEGER
);
CREATE TABLE IF NOT EXISTS comment (
    id INTEGER PRIMARY KEY,
    content TEXT,
    next_comment_id INTEGER
);