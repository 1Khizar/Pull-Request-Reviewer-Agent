import requests
from langchain_core.tools import tool
from config.settings import HEADERS

# =========================
# GitHub Tools
# =========================
@tool
def fetch_pull_request(owner: str, repo: str, pr_number: int) -> dict:
    """
    Fetch metadata and file-level details of a GitHub pull request.
    Returns title, description, author, branches, and changed files.
    """
    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    files_url = f"{pr_url}/files"

    pr = requests.get(pr_url, headers=HEADERS).json()
    if "message" in pr:
        return None

    files = requests.get(files_url, headers=HEADERS).json()
    if isinstance(files, dict) and "message" in files:
        return None

    return {
        "title": pr["title"],
        "description": pr["body"],
        "author": pr["user"]["login"],
        "base_branch": pr["base"]["ref"],
        "head_branch": pr["head"]["ref"],
        "files": [
            {"filename": f["filename"], "status": f["status"], "patch": f.get("patch", "")}
            for f in files
        ]
    }

@tool
def add_pull_request_comment(owner: str, repo: str, pr_number: int, comment: str) -> str:
    """
    Post a comment on a GitHub pull request.
    Returns status message indicating success or failure.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    payload = {"body": comment}
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        return "Comment posted successfully."
    elif response.status_code == 404:
        return "Pull Request not found or permission denied."
    return f"Failed to post comment: {response.json().get('message', response.text)}"
