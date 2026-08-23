import os
import requests
from datetime import datetime, timedelta, timezone

# Grab the secret token
TOKEN = os.getenv('GH_PAT')
headers = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}

import re

# Calculate exactly 24 hours ago
yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()

# Use PHT (UTC+8) for local date representation to align with the Action schedule
PHT = timezone(timedelta(hours=8))
today_str = datetime.now(PHT).strftime('%Y-%m-%d')

# Read existing commit SHAs to prevent duplicates
existing_shas = set()
has_today_header = False
if os.path.exists('audit.md'):
    try:
        with open('audit.md', 'r') as file:
            content = file.read()
            existing_shas = set(re.findall(r'`([0-9a-f]{7})`', content))
            has_today_header = f"## Activity for {today_str}" in content
    except Exception as e:
        print(f"Warning: Could not read audit.md for deduplication: {e}")

# Get all your repositories
response = requests.get('https://api.github.com/user/repos?per_page=100&sort=updated', headers=headers)
if response.status_code != 200:
    print(f"Error fetching repositories: {response.status_code} - {response.text}")
    exit(1)

repos = response.json()

new_commits_by_repo = {}
for repo in repos:
    repo_name = repo['full_name']
    
    # Ask the API for commits in this repo since yesterday
    commits_url = f"https://api.github.com/repos/{repo_name}/commits?since={yesterday}"
    commits_response = requests.get(commits_url, headers=headers)
    if commits_response.status_code != 200:
        continue
    commits = commits_response.json()
    
    if isinstance(commits, list):
        repo_commits = []
        for c in commits:
            sha = c['sha'][:7]
            if sha not in existing_shas:
                msg = c['commit']['message'].splitlines()[0] # Get the first line of the commit
                repo_commits.append((sha, msg))
        
        if repo_commits:
            new_commits_by_repo[repo['name']] = repo_commits

# Write to markdown file
if new_commits_by_repo:
    with open('audit.md', 'a') as file:
        # Write header if not already present for today
        if not has_today_header:
            file.write(f"\n## Activity for {today_str}\n\n")
        
        for repo_name, commits in new_commits_by_repo.items():
            file.write(f"### 📁 {repo_name}\n")
            for sha, msg in commits:
                file.write(f"- `{sha}`: {msg}\n")
            file.write("\n")
elif not has_today_header:
    # If no new commits and no header for today yet, write "No commits recorded" to maintain contribution streak
    with open('audit.md', 'a') as file:
        file.write(f"\n## Activity for {today_str}\n\n")
        file.write("*No commits recorded across repositories today.*\n")
else:
    print("No new activity to write.")