from config.settings import HEADERS
import requests
from urllib.parse import urlparse

# =========================
# Helpers
# =========================
def check_pr_exists(owner: str, repo: str, pr_number: int) -> bool:
    """Check if the GitHub PR exists."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    return requests.get(url, headers=HEADERS).status_code == 200

def parse_repo_link(link: str) -> dict:
    """Parse GitHub repo link to get owner and repo name."""
    path_parts = urlparse(link).path.strip("/").split("/")
    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub repo link")
    return {"owner": path_parts[0], "repo": path_parts[1]}