CREATE TABLE IF NOT EXISTS alert (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT,
    event_description TEXT,
    sender TEXT,
    event_loc TEXT,
    event_date TEXT,
    severity TEXT
)