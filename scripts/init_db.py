import sqlite3
import os

DB_PATH = os.getenv("DATABASE_PATH")

if not DB_PATH:
    raise RuntimeError("DATABASE_PATH must be set")

schema = """
CREATE TABLE IF NOT EXISTS tests (
    test_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    clinic_id TEXT NOT NULL,
    test_type TEXT NOT NULL,
    result TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(schema)
        conn.commit()
        print("Database initialized successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
