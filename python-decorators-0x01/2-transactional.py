import sqlite3
import functools
from datetime import datetime  # optional: for simple timestamped logs

# ---- Copied from Task 1 ----
def with_db_connection(func):
    """Open a SQLite connection, pass it as first arg (conn), and close it afterward."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Database connection closed.")
    return wrapper
# -----------------------------

def transactional(func):
    """
    Ensure the wrapped DB operation runs inside a transaction.
    - COMMIT if the function succeeds
    - ROLLBACK if any exception is raised, then re-raise
    Expects the first positional argument to be an open connection.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Transaction rolled back. Error: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update a user's email inside a managed transaction.
    Decorators:
      - with_db_connection: opens/closes SQLite connection
      - transactional: commits on success, rolls back on failure
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# ---- Example call (will COMMIT on success, ROLLBACK on error) ----
update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
