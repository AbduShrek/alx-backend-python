ChatGPT said:

Here’s Task 3 with retries fully implemented ✅

📄 3-retry_on_failure.py
import time
import sqlite3
import functools
from datetime import datetime


# ---- Copied from Task 1 (with_db_connection) ----
def with_db_connection(func):
    """Decorator to open/close SQLite connection and pass it to the function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Database connection closed.")
    return wrapper
# -------------------------------------------------


def retry_on_failure(retries=3, delay=2):
    """
    Retry decorator for transient DB errors.
    - retries: number of attempts before giving up
    - delay: seconds to wait between attempts
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] All {retries} attempts failed.")
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users with automatic retry on transient errors.
    - with_db_connection handles DB connection lifecycle
    - retry_on_failure retries query execution if it fails
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# ---- Example usage ----
users = fetch_users_with_retry()
print(users)
