#!/usr/bin/env python3
"""
Seed and prepare the ALX_prodev MySQL database.

Functions:
- connect_db() -> connects to the MySQL server (no DB selected)
- create_database(connection) -> creates ALX_prodev if it doesn't exist
- connect_to_prodev() -> connects specifically to the ALX_prodev database
- create_table(connection) -> creates user_data table if it doesn't exist
- insert_data(connection, csv_path) -> loads rows from CSV into user_data
"""

import os
import csv
from typing import Optional, Tuple

try:
    import mysql.connector  # type: ignore
    from mysql.connector.connection import MySQLConnection  # type: ignore
except Exception as e:  # pragma: no cover
    raise SystemExit(
        "mysql-connector-python is required. "
        "pip install mysql-connector-python\n"
        f"Original error: {e}"
    )


# --- Basic connection settings (override via env if needed) ---
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
DB_NAME = "ALX_prodev"


def _connect(
    db: Optional[str] = None
) -> Tuple[Optional[MySQLConnection], Optional[Exception]]:
    """Internal helper to create a MySQL connection."""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=db if db else None,
            autocommit=False,
        )
        return conn, None
    except Exception as err:
        return None, err


def connect_db() -> Optional[MySQLConnection]:
    """Connect to MySQL server (no database selected)."""
    conn, err = _connect(None)
    if err:
        print(f"Connection error: {err}")
        return None
    return conn


def create_database(connection: MySQLConnection) -> None:
    """Create the ALX_prodev database if it does not exist."""
    with connection.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    connection.commit()


def connect_to_prodev() -> Optional[MySQLConnection]:
    """Connect directly to the ALX_prodev database."""
    conn, err = _connect(DB_NAME)
    if err:
        print(f"Connection error (to {DB_NAME}): {err}")
        return None
    return conn


def create_table(connection: MySQLConnection) -> None:
    """Create user_data table if it does not exist (UUID PK + basic fields)."""
    with connection.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(10,2) NOT NULL
            );
            """
        )
    connection.commit()
    print("Table user_data created successfully")


def insert_data(connection: MySQLConnection, csv_path: str) -> None:
    """
    Insert rows from CSV into user_data.

    Expected CSV headers: user_id,name,email,age
    If a row with the same user_id exists, it will be updated.
    """
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            uid = r.get("user_id")
            name = r.get("name")
            email = r.get("email")
            # store age as numeric; if integer in CSV, it still fits DECIMAL
            age = r.get("age")
            if uid and name and email and age is not None:
                rows.append((uid, name, email, age))

    if not rows:
        return

    sql = (
        "INSERT INTO user_data (user_id, name, email, age) "
        "VALUES (%s, %s, %s, %s) "
        "ON DUPLICATE KEY UPDATE "
        "name=VALUES(name), email=VALUES(email), age=VALUES(age);"
    )

    with connection.cursor() as cur:
        cur.executemany(sql, rows)
    connection.commit()
