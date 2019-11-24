CREATE TABLE IF NOT EXISTS alert (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_zipcode TEXT,
    event_city TEXT,
    event_state TEXT,
    event_country TEXT,
    event_description TEXT,
    sender TEXT,
    event_date TEXT,
    severity TEXT
)