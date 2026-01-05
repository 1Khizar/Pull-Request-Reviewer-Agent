# 🤖 PullRequest Reviewer Agent

An **amazing, interactive, and beautiful** web interface for your AI-powered Pull Request Review Bot!

## ✨ Features

### 🎨 Stunning UI/UX

- **Animated gradient backgrounds** with floating orbs
- **Glassmorphism design** with backdrop blur effects
- **Smooth animations** on every interaction
- **Responsive design** that works on all devices
- **Interactive hover effects** and transitions
- **Modern color palette** with dark theme

### ⚡ User Experience

- **Real-time feedback** with loading animations
- **Clear error messages** for better debugging
- **Instant result display** with beautiful cards
- **Easy form reset** to review multiple PRs
- **Smooth scrolling** and page transitions

### 🚀 Functionality

- Submit GitHub repository URL and PR number
- AI-powered code review analysis
- Automatic GitHub comment posting
- Automatic Slack notifications
- Display comprehensive review results
- Status indicators for all operations

## 📁 Project Structure

```
your-project/
├── app.py                      # FastAPI backend server
├── main.py                     # Original CLI bot (unchanged)
├── helper.py                   # Helper functions (unchanged)
├── requirements.txt            # Python dependencies
├── static/
│   └── index.html             # Frontend HTML/CSS/JS
├── agent/                     # Your agent module (unchanged)
├── config/                    # Your config module (unchanged)
├── model/                     # Your model module (unchanged)
├── prompt/                    # Your prompt module (unchanged)
└── tools/                     # Your tools module (unchanged)
```

## 🛠️ Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Static Directory

The `app.py` file will automatically create the `static` directory, but you can create it manually:

```bash
mkdir static
```

## 🚀 Running the Application

### Start the FastAPI Server

```bash
python app.py
```

Or use uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Access the Web Interface

Open your browser and navigate to:

```
http://localhost:8000
```

## 🎯 How to Use

1. **Enter Repository URL**: Paste your GitHub repository URL
   - Example: `https://github.com/username/repository`

2. **Enter PR Number**: Type the pull request number you want to review
   - Example: `123`

3. **Click Review**: Hit the "🚀 Review Pull Request" button

4. **Wait for Results**: The bot will analyze the PR and show:
   - Complete AI-generated review
   - GitHub comment status
   - Slack notification status
   - Repository information

5. **Review Another PR**: Click "🔄 Review Another PR" to start over

## 🔧 API Endpoints

### `GET /`

Returns the main HTML interface

### `POST /api/review`

Submit a PR for review

**Request Body:**

```json
{
  "repo_link": "https://github.com/username/repo",
  "pr_number": 123
}
```

**Response:**

```json
{
  "success": true,
  "review": "AI-generated review text...",
  "github_status": "Comment posted successfully",
  "slack_status": "Message sent successfully",
  "pr_info": {
    "owner": "username",
    "repo": "repository",
    "pr_number": 123
  }
}
```

### `GET /api/health`

Health check endpoint

## 🎭 User Experience Highlights

1. **First Impression**: Beautiful animated background grabs attention immediately
2. **Clarity**: Clear labels and placeholders guide users
3. **Feedback**: Loading states show the bot is working
4. **Results**: Clean, organized display of review information
5. **Flow**: Easy to review multiple PRs without confusion

---

## 👨‍💻 About Me

**Made by Khizar Ishtiaq**

---
