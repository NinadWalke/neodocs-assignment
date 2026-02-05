import sqlite3
from contextlib import contextmanager
from app.config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def transaction():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN")
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
