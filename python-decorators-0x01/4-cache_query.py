import time
import sqlite3
import functools
from datetime import datetime

# Global cache dictionary
query_cache = {}


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


def cache_query(func):
    """
    Cache query results based on the SQL query string.
    - If the query result exists in cache, return it directly.
    - Otherwise, execute the function and cache the result.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        if not query and len(args) > 1:
            query = args[1]  # handle positional query after conn
        if query in query_cache:
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Returning cached result for query: {query}")
            return query_cache[query]
        # Run the actual function
        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Query cached: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users from DB with caching.
    - First call: executes SQL and caches result.
    - Next calls: return cached data for the same query.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# ---- Example usage ----
# First call will hit the DB and cache
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call will use the cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
