CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    phone TEXT NOT NULL,
    usertype TEXT NOT NULL,
    dob TEXT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)

DROP TABLE events;

CREATE TABLE IF NOT EXISTS events (
    eventID      INTEGER PRIMARY KEY AUTOINCREMENT,
    eventName    TEXT NOT NULL,
    eventYear    INTEGER,
    eventCountry TEXT,
    eventArea    TEXT,
    eventAreaPin INTEGER,
    eventStruct  TEXT,
    storageType  TEXT,
    storageKey   TEXT,
    created_by   TEXT NOT NULL,
    created_dt   TIMESTAMP NOT NULL,

    CONSTRAINT unique_event_per_user UNIQUE (eventName, created_by)
);