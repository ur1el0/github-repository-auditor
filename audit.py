import os
import requests
from datetime import datetime, timedelta, timezone

# Grab the secret token
TOKEN = os.getenv('GH_PAT')
headers = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}

# Calculate exactly 24 hours ago
yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
today_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')

# Get all your repositories
response = requests.get('https://api.github.com/user/repos?per_page=100&sort=updated', headers=headers)
if response.status_code != 200:
    print(f"Error fetching repositories: {response.status_code} - {response.text}")
    exit(1)

repos = response.json()

with open('audit.md', 'a') as file:
    file.write(f"\n## Activity for {today_str}\n\n")
    activity_found = False
    
    for repo in repos:
        repo_name = repo['full_name']
        
        # Ask the API for commits in this repo since yesterday
        commits_url = f"https://api.github.com/repos/{repo_name}/commits?since={yesterday}"
        commits = requests.get(commits_url, headers=headers).json()
        
        # If there are commits, write them to the markdown file
        if isinstance(commits, list) and len(commits) > 0:
            activity_found = True
            file.write(f"### 📁 {repo['name']}\n")
            for c in commits:
                msg = c['commit']['message'].splitlines()[0] # Get the first line of the commit
                sha = c['sha'][:7] # Get the short hash
                file.write(f"- `{sha}`: {msg}\n")
            file.write("\n")
    
    if not activity_found:
        file.write("*No commits recorded across repositories today.*\n")