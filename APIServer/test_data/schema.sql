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
)