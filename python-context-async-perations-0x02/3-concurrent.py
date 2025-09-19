import asyncio
import aiosqlite
from datetime import datetime

DB_PATH = "users.db"


async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Fetched all users: {len(rows)} rows")
            return [dict(r) for r in rows]


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Fetched users age > 40: {len(rows)} rows")
            return [dict(r) for r in rows]


async def fetch_concurrently():
    """Run both queries concurrently."""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results


if __name__ == "__main__":
    all_users, older_users = asyncio.run(fetch_concurrently())
    print("All users:", all_users)
    print("Users > 40:", older_users)
