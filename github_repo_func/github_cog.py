

import discord#type: ignore
from discord import app_commands#type: ignore
from discord.ext import commands#type: ignore


from .utils import parse_repo_link
from .github_api import github_api_request, get_commit_count,get_branch_count,get_pull_request_count
from .github_ui import create_repo_embed


class GithubAnalyzerCog(commands.Cog):
    
    def __init__(self,bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="repo",description="Analizeaza un repository Github.")
    @app_commands.describe(link="Link-ul complet al repository-ului GitHub")
    
    async def repo_stats(self,interaction:discord.Interaction,link:str):
        
        await interaction.response.defer()
        
        owner , repo = parse_repo_link(link)
        
        if not owner:
            await interaction.followup.send("Link Github invalid. Asigură-te că este în formatul corect.")
            return
        
        
        repo_data = github_api_request(f"{owner}/{repo}")
        
        if not repo_data or not isinstance(repo_data,dict):
            await interaction.followup.send("Nu am putut prelua datele repository-ului. Verifică dacă link-ul este corect și dacă repository-ul este public.")
            return
        
        commits= get_commit_count(owner,repo)
        branches= get_branch_count(owner,repo)
        pull_requests= get_pull_request_count(owner,repo)   
        
        embed = create_repo_embed(repo_data,link,branches,pull_requests,commits)
        await interaction.followup.send(embed=embed)
        