import discord #type: ignore
from discord import app_commands#type: ignore
from discord.ext import commands#type: ignore

from .db import create_task, get_all_tasks, init_db
from .ui import task_to_embed

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
