import aiosqlite
from datetime import datetime
from .model import Task

DB_PATH = "tasks.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            assigned_to TEXT,
            status TEXT,
            created_at TEXT
        )
        """)
        await db.commit()

async def create_task(title: str, description: str):
    async with aiosqlite.connect(DB_PATH) as db:
        created_at = datetime.now().isoformat()
        status = "pending"

        cursor = await db.execute("""
        INSERT INTO tasks (title, description, assigned_to, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (title, description, None, status, created_at))

        await db.commit()
        return cursor.lastrowid

async def get_task(task_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
        row = await cur.fetchone()
        if row:
            return Task(*row)
        return None

async def get_all_tasks():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT * FROM tasks ORDER BY task_id DESC")
        rows = await cur.fetchall()
        return [Task(*r) for r in rows]

async def assign_task(task_id: int, user_mention: str):
    """Assign a task to a user."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        UPDATE tasks 
        SET assigned_to = ?
        WHERE task_id = ?
        """, (user_mention, task_id))
        await db.commit()
        return await get_task(task_id)

async def update_task_status(task_id: int, status: str):
    """Update the status of a task."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        UPDATE tasks 
        SET status = ?
        WHERE task_id = ?
        """, (status, task_id))
        await db.commit()
        return await get_task(task_id)
