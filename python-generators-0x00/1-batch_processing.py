#!/usr/bin/env python3
"""
Batch streaming and processing of users from MySQL.

- stream_users_in_batches(batch_size): generator yielding lists of dict rows.
- batch_processing(batch_size): prints users with age > 25, batch by batch.
"""

import os
from typing import Generator, List, Dict, Any
import mysql.connector  # pip install mysql-connector-python


MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
DB_NAME = "ALX_prodev"


def stream_users_in_batches(batch_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Yield rows from user_data in batches (as a list of dicts).
    Uses a single loop overall (while True) to stream batches.
    """
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=DB_NAME,
    )
    # dictionary=True -> each row is a dict matching sample output
    cursor = conn.cursor(dictionary=True)
    try:
        # Cast age to integer in SQL to avoid Decimal in output
        cursor.execute(
            "SELECT user_id, name, email, CAST(age AS UNSIGNED) AS age "
            "FROM user_data ORDER BY user_id"
        )
        while True:  # loop #1
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows
    finally:
        try:
            cursor.close()
        finally:
            conn.close()


def batch_processing(batch_size: int) -> None:
    """
    Process users in batches, printing only users older than 25.
    Uses two loops: over batches, then over rows within each batch.
    """
    for batch in stream_users_in_batches(batch_size):  # loop #2
        for user in batch:  # loop #3
            if user.get("age", 0) > 25:
                print(user)
                print()  # match the blank line appearance in the sample run
