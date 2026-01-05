from model.llm import llm
from tools.github_tools import fetch_pull_request, add_pull_request_comment
from prompt.system_prompt import system_prompt
from langchain.agents import create_agent
from tools.slack_tool import send_slack_message

agent = create_agent(
    model=llm,
    tools=[fetch_pull_request, add_pull_request_comment, send_slack_message],
    system_prompt=system_prompt
)
