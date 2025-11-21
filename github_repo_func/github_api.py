import requests#type: ignore
import os
import re
from typing import Dict,Any,Optional


GITHUB_API_BASE = "https://api.github.com/repos"

def github_api_request(endpoint: str, is_full_url: bool = False, return_full_response: bool = False) -> Optional[requests.Response | Dict[str, Any]]:
    """Efectuează o cerere GET autentificată către GitHub API."""
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    if not GITHUB_TOKEN:
        print("Eroare: GITHUB TOKEN nu este setat.")
        return None
    
    url = endpoint if is_full_url else f"{GITHUB_API_BASE}/{endpoint}"
    
    
    headers ={
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        
        if return_full_response:
            return response
        else:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Eroare API GitHub la {url}: {e}")
        return None
    
    
    
def get_commit_count(owner:str,repo:str) -> int:
    
    endpoint = f"{owner}/{repo}/commits?per_page=1"
    
    
    response = github_api_request(endpoint,return_full_response=True)
    
    if response and isinstance(response,requests.Response) and 'Link' in response.headers:
        link_header = response.headers['Link']
        match = re.search(r'&page=(\d+)>; rel="last"',link_header)
        if match:
            return int(match.group(1))
        
    if response and isinstance(response,requests.Response) and response.status_code == 200:
        try:
            return len(response.json())
        except Exception:
            return 0
        
    return 0



def get_branch_count(owner: str, repo: str) -> int:
    """Numără exact branch-urile folosind header-ul Link pentru paginare."""
    
    # Endpointul: cerem o singură intrare pe pagină pentru a forța GitHub să ne dea link-ul 'last'
    endpoint = f"{owner}/{repo}/branches?per_page=1"
    
   
    response = github_api_request(endpoint, return_full_response=True) 
    
    if response and isinstance(response, requests.Response) and 'Link' in response.headers:
        link_header = response.headers['Link']
        
        # Caută link-ul către ULTIMA pagină (rel="last")
        match = re.search(r'page=(\d+)>; rel="last"', link_header)
        
        if match:
            # Numărul ultimei pagini este numărul total de branch-uri
            return int(match.group(1))
        
    # Dacă nu există header 'Link', înseamnă că sunt puține branch-uri (sau 0)
    if response and isinstance(response, requests.Response) and response.status_code == 200:
         try:
             
             return len(response.json())
         except Exception:
             return 0

    return 0


def get_pull_request_count(owner: str, repo: str) -> int:
    """Numără exact pull request-urile folosind header-ul Link pentru paginare."""
    
    endpoint = f"{owner}/{repo}/pulls?state=all&per_page=1"
    
    response = github_api_request(endpoint, return_full_response=True)
    
    if response and isinstance(response, requests.Response) and 'Link' in response.headers:
        link_header = response.headers['Link']
        
        match = re.search(r'page=(\d+)>; rel="last"', link_header)
        
        if match:
            return int(match.group(1))
        
    if response and isinstance(response, requests.Response) and response.status_code == 200:
        try:
            return len(response.json())
        except Exception:
            return 0
        
    return 0