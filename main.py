import discord # type: ignore
from discord.ext import commands # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

from func.team_task.task_commands import TaskCommands # type: ignore

@bot.event
async def on_ready():
    print(f"Bot conectat ca {bot.user}")

    synced = await bot.tree.sync()
    print(f"Comenzi slash sincronizate: {len(synced)}")


@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

@bot.command()
async def salut(ctx):
    await ctx.send("salut si tie!")


async def setup():
    """Încărcăm COG-urile înainte ca botul să pornească."""
    await bot.add_cog(TaskCommands(bot))

async def main():
    async with bot:
        await setup()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())

# ============================================================================
# COMPLETED TASK MANAGEMENT FUNCTIONALITY
# ============================================================================
# The following slash commands are now fully implemented and functional:
#
# 1. /task_new <title> <description>
#    - Creates a new task with the given title and description
#    - Status is set to "pending" by default
#    - Returns the task ID of the newly created task
#
# 2. /task_list
#    - Lists all tasks in the database
#    - Displays tasks as embedded messages with color-coded status
#    - Shows task ID, title, description, assigned user, status, and creation date
#
# 3. /task_assign <task_id> <user>
#    - Assigns a task to a specific Discord user
#    - Uses Discord member mention for assignment
#    - Updates the assigned_to field in the database
#
# 4. /task_done <task_id>
#    - Marks a task as completed (status: "done")
#    - Changes the task status to "done" in the database
#    - Provides confirmation message
#
# 5. /task_progress <task_id>
#    - Marks a task as in progress (status: "in_progress")
#    - Updates task status to show work has started
#    - Provides confirmation message
#
# Database Structure:
# - tasks.db contains a 'tasks' table with fields:
#   * task_id (INTEGER PRIMARY KEY AUTOINCREMENT)
#   * title (TEXT NOT NULL)
#   * description (TEXT)
#   * assigned_to (TEXT) - stores Discord user mention
#   * status (TEXT) - values: "pending", "in_progress", "done"
#   * created_at (TEXT) - ISO format timestamp
#
# All functions use aiosqlite for async database operations.
# UI provides color-coded embeds: gold for pending, blue for in_progress, green for done.
# ============================================================================
#
#
#