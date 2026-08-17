---
name: system-intel-scanner
description: "Extract useful repositories, solutions, and media for system development. Scans GitHub, StackOverflow, browser history, YouTube videos/shorts/reels, and curated tech sources. Use for self-improvement and research pipeline."
version: 1.0.1
trigger: "scan for repos", "scan stackoverflow", "scan youtube", "browser scan", "system intel", "research for Evelyn"
---

# System Intel Scanner

Unified extractor for Hermes/Evelyn system improvement.

## How to run when triggered

Use available tools to execute these steps in order.

### Step 1: Source scans via web_search
For each query, run web_search on the specified sources and collect raw results.

Queries:
- Hermes agent Evelyn
- AI agent automation  
- Python automation tools
- free LLM API routing
- Telegram Discord bot integrations
- Obsidian knowledge management
- GitHub Actions CI/CD
- system self-improvement

Sources:
- GitHub: web_search("site:github.com <query> stars:>50")
- StackOverflow: web_search("site:stackoverflow.com <query>")
- YouTube: web_search("site:youtube.com <query>")
- Reddit: web_search("site:reddit.com <query>")
- Hacker News: web_search("news.ycombinator.com <query>")
- PyPI: web_search("site:pypi.org <query>")
- npm: web_search("site:npmjs.com <query>")

### Step 2: Browser history scan
Run this via terminal():
```bash
python3 -c "
import sqlite3, json
from pathlib import Path
from datetime import datetime

output = []
keywords = ['AI','GPT','Claude','OpenAI','Anthropic','Hermes','Evelyn','agent','automation','Python','JavaScript','API','GitHub','StackOverflow','tutorial','YouTube','video','short','reel']
browsers = {
  'Chrome': Path.home() / 'AppData/Local/Google/Chrome/User Data/Default/History',
  'Edge': Path.home() / 'AppData/Local/Microsoft/Edge/User Data/Default/History',
  'Brave': Path.home() / 'AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/History',
}
for browser_name, history_path in browsers.items():
  if not history_path.exists(): continue
  conn = sqlite3.connect(str(history_path))
  cursor = conn.cursor()
  cursor.execute('SELECT url, title, last_visit_time, visit_count FROM urls WHERE last_visit_time > (strftime(\"%s\",\"now\") - 86400) * 1000000 ORDER BY last_visit_time DESC LIMIT 200')
  for url, title, ts, visits in cursor.fetchall():
    text = f'{(title or \"\").lower()} {(url or \"\").lower()}'
    if any(k.lower() in text for k in keywords):
      output.append({'source': f'browser-{browser_name}', 'title': title, 'url': url, 'timestamp': ts, 'visit_count': visits})
  conn.close()
print(json.dumps(output))
"
```

### Step 3: YouTube transcript extraction
For YouTube URLs found, extract transcripts using youtube-transcript-pro:
```bash
python3 "$LOCALAPPDATA/hermes/skills/youtube-transcript-pro/scripts/fetch_transcript.py" "<URL>" --text-only
```

### Step 4: Deduplicate and score
Combine all results, deduplicate by URL/title, filter for Hermes/Evelyn relevance.

### Step 5: Save and push
Write results to: `C:\Users\My PC\AppData\Local\hermes\data\intel-scans\scan-YYYYMMDD-HHMMSS.json`

If results found, copy relevant items to:
- `C:\Users\My PC\OneDrive\Desktop\AI-Ops-Vault\intel\scan-YYYYMMDD-HHMMSS.md`
- `C:\Users\My PC\OneDrive\Desktop\PAIOS\intel\scan-YYYYMMDD-HHMMSS.md`

Then commit and push from each vault:
```bash
git add -A && git commit -m "chore(intel): auto-sync system intel <timestamp>" && git push origin <current-branch>
```

## Scheduling
Daily at 06:00 via Hermes cron job.
