import sqlite3
import functools
from datetime import datetime   # Optional for logging timestamps

# Decorator to automatically handle DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open connection before the function runs
        conn = sqlite3.connect("users.db")
        try:
            # Pass the connection object to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Always close connection, even if error occurs
            conn.close()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Database connection closed.")
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a user by ID using the provided database connection.
    Connection is automatically managed by the with_db_connection decorator.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Example usage
user = get_user_by_id(user_id=1)
print(user)
