from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from helper import parse_repo_link, check_pr_exists
from agent.agent import agent
from langchain_core.messages import HumanMessage
from tools.github_tools import add_pull_request_comment
from tools.slack_tool import send_slack_message
import os
import json
from datetime import datetime
from typing import List, Optional

app = FastAPI(title="PullRequest Reviewer Agent")

# In-memory storage for review history
review_history = []

# Serve static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class PRReviewRequest(BaseModel):
    repo_link: str
    pr_number: int

class ReviewHistoryItem(BaseModel):
    id: int
    timestamp: str
    repo_name: str
    pr_number: int
    review_summary: str
    github_comment_added: bool
    slack_message_sent: bool
    status: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/review")
async def review_pr(request: PRReviewRequest):
    try:
        # Clean repo link
        repo_link = request.repo_link.strip()
        if repo_link.endswith(".git"):
            repo_link = repo_link[:-4]
        
        # Parse repository
        owner_repo = parse_repo_link(repo_link)
        
        # Check if PR exists
        if not check_pr_exists(owner_repo["owner"], owner_repo["repo"], request.pr_number):
            raise HTTPException(status_code=404, detail=f"Pull Request #{request.pr_number} does not exist")
        
        # Generate PR Review
        response = agent.invoke({
            "messages": [
                HumanMessage(content=f"Please review PR #{request.pr_number} from repository {repo_link}")
            ]
        })
        review_text = response["messages"][-1].content
        
        # Post GitHub Comment
        github_success = False
        github_message = ""
        try:
            status_message = "✅ Pull request review completed successfully by PullRequest Reviewer Agent."
            github_result = add_pull_request_comment.invoke({
                "owner": owner_repo["owner"],
                "repo": owner_repo["repo"],
                "pr_number": request.pr_number,
                "comment": status_message
            })
            github_success = True
            github_message = "Comment added successfully"
        except Exception as e:
            github_message = f"Failed to add comment: {str(e)}"
        
        # Send Slack Message
        slack_success = False
        slack_message = ""
        try:
            slack_result = send_slack_message.invoke(f"🤖 PR #{request.pr_number} Review:\n\n{review_text}")
            slack_success = True
            slack_message = "Message sent successfully"
        except Exception as e:
            slack_message = f"Failed to send message: {str(e)}"
        
        # Create review summary (first 150 chars)
        review_summary = review_text[:150] + "..." if len(review_text) > 150 else review_text
        
        # Add to history
        history_item = {
            "id": len(review_history) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "repo_name": f"{owner_repo['owner']}/{owner_repo['repo']}",
            "pr_number": request.pr_number,
            "review_summary": review_summary,
            "review_full": review_text,
            "github_comment_added": github_success,
            "slack_message_sent": slack_success,
            "github_message": github_message,
            "slack_message": slack_message,
            "status": "completed"
        }
        review_history.insert(0, history_item)  # Add to beginning
        
        # Keep only last 50 reviews
        if len(review_history) > 50:
            review_history.pop()
        
        return {
            "success": True,
            "review": review_text,
            "github_status": github_message,
            "github_success": github_success,
            "slack_status": slack_message,
            "slack_success": slack_success,
            "pr_info": {
                "owner": owner_repo["owner"],
                "repo": owner_repo["repo"],
                "pr_number": request.pr_number
            },
            "history_id": history_item["id"]
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/api/history")
async def get_history():
    """Get all review history"""
    return {"history": review_history, "total": len(review_history)}

@app.get("/api/history/{review_id}")
async def get_review_detail(review_id: int):
    """Get detailed review by ID"""
    for review in review_history:
        if review["id"] == review_id:
            return review
    raise HTTPException(status_code=404, detail="Review not found")

@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    total_reviews = len(review_history)
    github_success = sum(1 for r in review_history if r.get("github_comment_added", False))
    slack_success = sum(1 for r in review_history if r.get("slack_message_sent", False))
    
    # Get unique repos
    unique_repos = len(set(r["repo_name"] for r in review_history))
    
    # Get today's reviews
    today = datetime.now().strftime("%Y-%m-%d")
    today_reviews = sum(1 for r in review_history if r["timestamp"].startswith(today))
    
    return {
        "total_reviews": total_reviews,
        "github_comments": github_success,
        "slack_messages": slack_success,
        "unique_repositories": unique_repos,
        "today_reviews": today_reviews,
        "success_rate": round((github_success / total_reviews * 100) if total_reviews > 0 else 0, 1)
    }

@app.delete("/api/history/{review_id}")
async def delete_review(review_id: int):
    """Delete a review from history"""
    global review_history
    review_history = [r for r in review_history if r["id"] != review_id]
    return {"success": True, "message": "Review deleted"}

@app.delete("/api/history")
async def clear_history():
    """Clear all history"""
    global review_history
    review_history = []
    return {"success": True, "message": "History cleared"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "PullRequest Reviewer Agent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)