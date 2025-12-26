CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    phone TEXT NOT NULL,
    usertype TEXT NOT NULL,
    dob TEXT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        eventname TEXT UNIQUE,
        data TEXT
    )

