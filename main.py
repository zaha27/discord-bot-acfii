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