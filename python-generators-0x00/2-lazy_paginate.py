#!/usr/bin/env python3
"""
Lazy pagination over user_data using a generator.

- paginate_users(page_size, offset): fetches one page from the DB.
- lazy_pagination(page_size): yields each page only when needed.
  (Single loop total; uses yield.)
"""

from typing import List, Dict, Any, Generator
import seed


def paginate_users(page_size: int, offset: int) -> List[Dict[str, Any]]:
    """
    Fetch a single page from user_data with the given size and offset.
    Returns a list of dictionaries (rows). Does not keep the connection open.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            f"SELECT user_id, name, email, CAST(age AS UNSIGNED) AS age "
            f"FROM user_data LIMIT {page_size} OFFSET {offset}"
        )
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        connection.close()


def lazy_pagination(page_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Lazily yield pages of users. Starts at offset 0 and fetches the next page
    *only* when the consumer asks for it. Uses exactly one loop.
    """
    offset = 0
    while True:  # single loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# Alias to match the sample main:
#   from 2-lazy_paginate import lazy_pagination
lazy_paginate = lazy_pagination
