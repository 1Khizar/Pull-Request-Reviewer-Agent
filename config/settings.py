import os

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# GitHub Settings
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Slack Settings
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

# LLM API Key
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

