# 📡 GitHub Webhook Listener (Webhook-Repo)

This Flask application receives GitHub webhook events (`Push`, `Pull Request`, `Merge`) from another GitHub repository (`action-repo`), stores them in MongoDB, and displays them live on a web UI.

---

## 📌 Features

✅ Handles the following GitHub events:
- `PUSH`
- `PULL_REQUEST`
- `MERGE` (when a PR is merged)

✅ Stores event data in MongoDB using a defined schema  
✅ Frontend auto-refreshes every 15 seconds to show the latest activities

---

## 🧠 MongoDB Schema

Each webhook event is stored in this format:

| Field         | Type               | Description                                     |
|---------------|--------------------|-------------------------------------------------|
| `_id`         | ObjectId           | MongoDB's default ID                            |
| `request_id`  | string             | Git commit hash (for push) or PR ID             |
| `author`      | string             | GitHub user who triggered the event             |
| `action`      | string             | `"PUSH"`, `"PULL_REQUEST"`, or `"MERGE"`        |
| `from_branch` | string             | Source branch (for PR and Merge events)         |
| `to_branch`   | string             | Target branch                                   |
| `timestamp`   | string (datetime)  | UTC-formatted timestamp of the event            |

---

## 🚀 How to Run

### 🔧 Requirements

- Python 3.8+
- MongoDB (local or MongoDB Atlas)
- pip

### 🛠️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/webhook-repo.git
   cd webhook-repo
