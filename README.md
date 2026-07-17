# GitHub Daily Auditor

An automated tracker that scans all of my GitHub repositories daily, logs the most recent commit activity, and compiles it into a central Markdown file.

Not only does this provide a clean, centralized audit log of my daily coding activity, but the automated daily push also effortlessly maintains my GitHub contribution streak.

## Features
* **Global Account Auditing:** Uses the GitHub API to check all repositories (public and private) for recent activity.
* **Automated Logging:** Appends a clean, formatted summary of the day's commits directly to `audit.md`.
* **Streak Maintenance:** Runs reliably on a schedule via GitHub Actions, securing a daily contribution square.
* **Zero Maintenance:** Once the Personal Access Token (PAT) is provided, the Python script and GitHub Action handle everything completely hands-off.

## How It Works
1. A **GitHub Action** triggers a cron job every day.
2. The Action spins up an Ubuntu runner and executes `audit.py`.
3. The Python script authenticates using a repository secret (`GH_PAT`) and fetches all commits made across my account within the last 24 hours.
4. The findings are appended to `audit.md`.
5. A bot automatically commits and pushes the updated `.md` file to this repository.

##  Setup Instructions (If you want to fork this)
If you want to run your own auditor:
1. Clone or fork this repository.
2. Go to your GitHub **Developer Settings** and generate a new **Personal Access Token (classic)** with the `repo` scope enabled.
3. Go to this repository's **Settings > Secrets and variables > Actions** and create a new repository secret named `GH_PAT`. Paste your token there.
4. The Action will automatically run at the scheduled time, or you can trigger it manually via the **Actions** tab.