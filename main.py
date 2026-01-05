from helper import parse_repo_link, check_pr_exists
from agent.agent import agent
from langchain_core.messages import HumanMessage
from tools.github_tools import add_pull_request_comment
from tools.slack_tool import send_slack_message

# =========================
# Run Bot
# =========================
repo_link = input("Enter the Repo link: ").strip()
pr_number = int(input("Enter the Pull Request number: ").strip())

if repo_link.endswith(".git"):
    repo_link = repo_link[:-4]

owner_repo = parse_repo_link(repo_link)

if not check_pr_exists(owner_repo["owner"], owner_repo["repo"], pr_number):
    print(f"\nPull Request #{pr_number} does not exist.")
else:
    # Generate PR Review
    response = agent.invoke({
        "messages": [
            HumanMessage(content=f"Please review PR #{pr_number} from repository {repo_link}")
        ]
    })
    review_text = response["messages"][-1].content
    print("\n===== PR REVIEW =====\n")
    print(review_text)

    # Post GitHub Comment
    status_message = "✅ Pull request review completed successfully."
    github_result = add_pull_request_comment.invoke({
        "owner": owner_repo["owner"],
        "repo": owner_repo["repo"],
        "pr_number": pr_number,
        "comment": status_message
    })
    print("\n===== GITHUB COMMENT STATUS =====\n", github_result)

    # Send Slack Message
    slack_result = send_slack_message.invoke(f"PR #{pr_number} Review:\n{review_text}")
    print("\n===== SLACK STATUS =====\n", slack_result)