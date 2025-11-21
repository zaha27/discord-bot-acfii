import discord # type: ignore
from discord import app_commands # type: ignore
from discord.ext import commands # type: ignore 

from .db import create_task, get_all_tasks, init_db, assign_task, update_task_status, get_task
from .ui import task_to_embed
from .model import STATUS_IN_PROGRESS, STATUS_DONE

class TaskCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await init_db()

    @app_commands.command(name="task_new", description="Creeaza un task nou")
    async def task_new(self, interaction: discord.Interaction, title: str, description: str):
        task_id = await create_task(title, description)
        await interaction.response.send_message(f"✅ Task creat cu ID **{task_id}**")

    @app_commands.command(name="task_list", description="Lista cu toate task-urile")
    async def task_list(self, interaction: discord.Interaction):
        tasks = await get_all_tasks()

        if not tasks:
            return await interaction.response.send_message("Nu exista task-uri.")

        embeds = [task_to_embed(t) for t in tasks]

        await interaction.response.send_message(embeds=embeds)

    @app_commands.command(name="task_assign", description="Asigneaza un task unui user")
    async def task_assign(self, interaction: discord.Interaction, task_id: int, user: discord.Member):
        task = await assign_task(task_id, user.mention)
        
        if task:
            await interaction.response.send_message(f"✅ Task **#{task_id}** asignat lui {user.mention}")
        else:
            await interaction.response.send_message(f"❌ Task-ul cu ID **{task_id}** nu exista.")

    @app_commands.command(name="task_done", description="Marcheaza un task ca fiind finalizat")
    async def task_done(self, interaction: discord.Interaction, task_id: int):
        task = await update_task_status(task_id, STATUS_DONE)
        
        if task:
            await interaction.response.send_message(f"✅ Task **#{task_id}** marcat ca finalizat!")
        else:
            await interaction.response.send_message(f"❌ Task-ul cu ID **{task_id}** nu exista.")

    @app_commands.command(name="task_progress", description="Marcheaza un task ca fiind in progres")
    async def task_progress(self, interaction: discord.Interaction, task_id: int):
        task = await update_task_status(task_id, STATUS_IN_PROGRESS)
        
        if task:
            await interaction.response.send_message(f"✅ Task **#{task_id}** marcat ca in progres!")
        else:
            await interaction.response.send_message(f"❌ Task-ul cu ID **{task_id}** nu exista.")
