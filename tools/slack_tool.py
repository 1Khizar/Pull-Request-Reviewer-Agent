import requests
from langchain_core.tools import tool
from config.settings import SLACK_TOKEN, SLACK_CHANNEL

# =========================
# Slack Tool
# =========================
@tool
def send_slack_message(message: str) -> str:
    """
    Send a message to a Slack channel using the Slack Bot token.
    Returns status message indicating success or failure.
    """
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    payload = {"channel": SLACK_CHANNEL, "text": message}

    response = requests.post(url, headers=headers, json=payload).json()
    if response.get("ok"):
        return "Slack message sent successfully."
    return f"Failed to send Slack message: {response.get('error', 'Unknown error')}"
