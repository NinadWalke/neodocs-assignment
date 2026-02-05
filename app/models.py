from datetime import datetime
import sqlite3
from app.db import transaction


def insert_test(payload: dict) -> None:
    sql = """
    INSERT INTO tests (
        test_id,
        patient_id,
        clinic_id,
        test_type,
        result,
        created_at
    ) VALUES (?, ?, ?, ?, ?, ?)
    """

    values = (
        payload["test_id"],
        payload["patient_id"],
        payload["clinic_id"],
        payload["test_type"],
        payload["result"],
        datetime.utcnow().isoformat(),
    )

    with transaction() as cursor:
        cursor.execute(sql, values)


def get_tests_by_clinic(clinic_id: str) -> list[dict]:
    sql = """
    SELECT
        test_id,
        patient_id,
        clinic_id,
        test_type,
        result,
        created_at
    FROM tests
    WHERE clinic_id = ?
    """

    with transaction() as cursor:
        cursor.execute(sql, (clinic_id,))
        rows = cursor.fetchall()

    return [dict(row) for row in rows]
