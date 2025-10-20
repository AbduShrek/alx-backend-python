#!/usr/bin/env python3
"""
Stream users from MySQL one-by-one using a Python generator.

Connects to the ALX_prodev DB and yields rows from user_data as dicts.
Environment vars (optional): MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD
"""

import os
from typing import Generator, Dict, Any
from decimal import Decimal

import mysql.connector  # pip install mysql-connector-python


MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
DB_NAME = "ALX_prodev"


def _normalize_age(value: Any) -> Any:
    """Convert Decimal ages to int (if integral) or float for clean printing."""
    if isinstance(value, Decimal):
        try:
            i = int(value)
            return i if value == i else float(value)
        except Exception:
            return float(value)
    return value


def stream_users() -> Generator[Dict[str, Any], None, None]:
    """
    Yield rows from user_data as dictionaries, one by one.
    Uses exactly one loop over the cursor.
    """
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=DB_NAME,
    )
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT user_id, name, email, age FROM user_data ORDER BY user_id"
        )
        for row in cursor:  # <-- single loop
            row = dict(row)
            row["age"] = _normalize_age(row.get("age"))
            yield row
    finally:
        try:
            cursor.close()
        finally:
            conn.close()
