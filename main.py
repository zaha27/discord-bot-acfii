

import discord#type: ignore
from discord.ext import commands#type: ignore
from dotenv import load_dotenv#type: ignore
import os
import asyncio 


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 1. Importul COG-urilor
from func.team_task.task_commands import TaskCommands 

from github_repo_func.github_cog import GithubAnalyzerCog
@bot.event
async def on_ready():
    print(f"Bot conectat ca {bot.user}")
    
    #  Sincronizarea este esențială pentru a înregistra /repo, /task_list, și /task_new
    try:
        
        synced = await bot.tree.sync()
        print(f"Comenzi slash sincronizate: {len(synced)}")
    except Exception as e:
        print(f"Eroare la sincronizarea comenzilor: {e}")


# --- Comenzile Prefixate Defined Directly in main.py (Conform Structurii Originale) ---

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

@bot.command()
async def salut(ctx):
    await ctx.send("salut si tie!")




async def setup_cogs():
    """Încărcăm toate COG-urile înainte ca botul să pornească."""
    
    # 2. Adaug COG-ul existent (TaskCommands)
    try:
        await bot.add_cog(TaskCommands(bot))
        print("TaskCommands COG încărcat.")
    except Exception as e:
        print(f"Eroare la încărcarea TaskCommands: {e}")
        
    # 3. Adaug noul COG (GithubAnalyzerCog)
    try:
        await bot.add_cog(GithubAnalyzerCog(bot))
        print("GithubAnalyzerCog COG încărcat.")
    except Exception as e:
        print(f"Eroare la încărcarea GithubAnalyzerCog: {e}")




async def main():
   
    await setup_cogs() 
    
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Botul a fost oprit.")
    except Exception as e:
        print(f"O eroare a apărut la rularea botului: {e}")