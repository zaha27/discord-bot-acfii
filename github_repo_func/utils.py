import re
from typing import Tuple

def parse_repo_link(link: str) -> Tuple[str,str] :
    """Extrage owner și repo din link-ul GitHub."""
    
    match=re.search(r'github\.com/([^/]+)/([^/]+)',link)
    if match:
        return match.group(1),match.group(2)
    return "", ""

