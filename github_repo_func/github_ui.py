

import discord#type: ignore
from typing import Dict, Any

def create_repo_embed(repo_data: Dict[str, Any], link: str, branches: int, pull_requests: int, commits: int) -> discord.Embed:
    """Creează și formatează obiectul discord.Embed pentru rezultatele repo-ului."""
    
    repo_name = repo_data.get("name", "N/A")
    owner = repo_data.get("owner", {}).get("login", "N/A")
    description = repo_data.get("description", "Fără descriere.")
    stars = repo_data.get('stargazers_count', 0)
    forks = repo_data.get('forks_count', 0)
    language = repo_data.get('language', 'N/A')
    open_issues = repo_data.get('open_issues_count', 0)
    
    embed = discord.Embed(
        title=f"📊 Analiza Repository: {owner}/{repo_name}",
        description=description,
        url=link,
        color=discord.Color.blue()
    )
    
    
    embed.add_field(name="🌱 Branch-uri", value=f"{branches}", inline=True)
    embed.add_field(name="💬 Pull Requests", value=f"{pull_requests}", inline=True)
    embed.add_field(name="💾 Commit-uri", value=f"{commits}", inline=True)
    
    embed.add_field(name="⭐ Stele", value=f"{stars}", inline=True)
    embed.add_field(name="🍴 Forks", value=f"{forks}", inline=True)
    embed.add_field(name="💻 Limbaj Principal", value=f"{language}", inline=True)
    
    return embed