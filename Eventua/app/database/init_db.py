
# python database/init_db.py

import sqlite3

def initialize_db(db_path="database/sqlite.db", schema_path="database/schema.sql"):
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, "r") as f:
            ddl = f.read()
        conn.executescript(ddl)
        print("Database initialized with schema.")

if __name__ == "__main__":
    initialize_db()