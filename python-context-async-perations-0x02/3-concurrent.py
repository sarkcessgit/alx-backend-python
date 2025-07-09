#!/usr/bin/env python3
"""
3-concurrent.py - Concurrent asynchronous database queries using aiosqlite and asyncio.gather.
"""

import asyncio
import aiosqlite

DB_NAME = "users.db"

async def async_fetch_users():
    """
    Asynchronously fetches all users from the database.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All Users:")
            for row in results:
                print(row)
            return results

async def async_fetch_older_users():
    """
    Asynchronously fetches users older than 40.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in results:
                print(row)
            return results

async def fetch_concurrently():
    """
    Run both queries concurrently using asyncio.gather().
    """
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# ✅ Run the concurrent tasks
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
