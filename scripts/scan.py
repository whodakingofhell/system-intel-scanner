#!/usr/bin/env python3
"""System Intel Scanner - unified extractor for system development intelligence."""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from hermes_tools import web_search, terminal
except Exception as e:
    print(f"ERROR: Cannot import hermes_tools: {e}")
    sys.exit(1)

OUTPUT_DIR = Path.home() / "AppData/Local/hermes/data/intel-scans"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def save_results(name, results):
    path = OUTPUT_DIR / f"{name}-{timestamp()}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {len(results)} items -> {path}")
    return path

def search_github(query, limit=10):
    results = []
    try:
        data = web_search(f"site:github.com {query} stars:>50", limit=limit)
        for item in data.get("data", {}).get("web", []):
            results.append({
                "source": "github",
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
                "found_at": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"github scan error: {e}")
    return results

def search_stackoverflow(query, limit=10):
    results = []
    try:
        data = web_search(f"site:stackoverflow.com {query}", limit=limit)
        for item in data.get("data", {}).get("web", []):
            results.append({
                "source": "stackoverflow",
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
                "found_at": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"stackoverflow scan error: {e}")
    return results

def search_youtube(query, limit=10):
    results = []
    try:
        data = web_search(f"site:youtube.com {query}", limit=limit)
        for item in data.get("data", {}).get("web", []):
            results.append({
                "source": "youtube",
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
                "found_at": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"youtube scan error: {e}")
    return results

def search_reddit(query, limit=10):
    results = []
    try:
        data = web_search(f"site:reddit.com {query}", limit=limit)
        for item in data.get("data", {}).get("web", []):
            results.append({
                "source": "reddit",
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
                "found_at": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"reddit scan error: {e}")
    return results

def search_hackernews(query, limit=10):
    results = []
    try:
        data = web_search(f"site:news.ycombinator.com {query}", limit=limit)
        for item in data.get("data", {}).get("web", []):
            results.append({
                "source": "hackernews",
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
                "found_at": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"hackernews scan error: {e}")
    return results

def search_pypi(query, limit=10):
    results = []
    try:
        data = web_search(f"site:pypi.org {query}", limit=limit)
        for item in data.get("data", {}).get("web", []):
            results.append({
                "source": "pypi",
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
                "found_at": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"pypi scan error: {e}")
    return results

def search_npm(query, limit=10):
    results = []
    try:
        data = web_search(f"site:npmjs.com {query}", limit=limit)
        for item in data.get("data", {}).get("web", []):
            results.append({
                "source": "npm",
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
                "found_at": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"npm scan error: {e}")
    return results

def scan_browser_history():
    results = []
    try:
        import sqlite3
        from pathlib import Path
        browsers = {
            "Chrome": Path.home() / "AppData/Local/Google/Chrome/User Data/Default/History",
            "Edge": Path.home() / "AppData/Local/Microsoft/Edge/User Data/Default/History",
            "Brave": Path.home() / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/History",
        }
        keywords = [
            "AI", "artificial intelligence", "machine learning", "GPT", "Claude",
            "OpenAI", "Anthropic", "Hermes", "Evelyn", "agent", "automation",
            "Python", "JavaScript", "TypeScript", "API", "integration",
            "GitHub", "StackOverflow", "tutorial", "guide", "documentation",
            "YouTube", "reel", "short", "video"
        ]
        for browser_name, history_path in browsers.items():
            if not history_path.exists():
                continue
            try:
                conn = sqlite3.connect(str(history_path))
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT url, title, last_visit_time, visit_count
                    FROM urls
                    WHERE last_visit_time > (strftime('%s', 'now') - 86400) * 1000000
                    ORDER BY last_visit_time DESC
                    LIMIT 200
                """)
                for row in cursor.fetchall():
                    title = (row[1] or "").lower()
                    url = (row[0] or "").lower()
                    if any(kw.lower() in title or kw.lower() in url for kw in keywords):
                        results.append({
                            "source": f"browser-{browser_name}",
                            "title": row[1],
                            "url": row[0],
                            "timestamp": row[2],
                            "visit_count": row[3],
                            "found_at": datetime.now().isoformat()
                        })
                conn.close()
            except Exception as e:
                print(f"browser scan error {browser_name}: {e}")
    except Exception as e:
        print(f"browser history import error: {e}")
    return results

def dedupe(results):
    seen = set()
    out = []
    for r in results:
        key = (r.get("url") or r.get("title") or "").strip()
        if key and key not in seen:
            seen.add(key)
            out.append(r)
    return out

def main():
    sources = sys.argv[1:] if len(sys.argv) > 1 else ["github", "stackoverflow", "youtube", "browser", "reddit", "hackernews", "pypi", "npm"]
    queries = [
        "Hermes agent Evelyn",
        "AI agent automation",
        "Python automation tools",
        "free LLM API routing",
        "Telegram Discord bot integrations",
        "Obsidian knowledge management",
        "GitHub Actions CI/CD",
        "system self-improvement"
    ]
    all_results = []
    print(f"Sources: {', '.join(sources)}")
    print(f"Queries: {len(queries)}")
    for q in queries:
        print(f"\nScanning: {q}")
        if "github" in sources:
            all_results.extend(search_github(q))
        if "stackoverflow" in sources:
            all_results.extend(search_stackoverflow(q))
        if "youtube" in sources:
            all_results.extend(search_youtube(q))
        if "reddit" in sources:
            all_results.extend(search_reddit(q))
        if "hackernews" in sources:
            all_results.extend(search_hackernews(q))
        if "pypi" in sources:
            all_results.extend(search_pypi(q))
        if "npm" in sources:
            all_results.extend(search_npm(q))
    if "browser" in sources:
        print("\nScanning browser history...")
        all_results.extend(scan_browser_history())
    all_results = dedupe(all_results)
    path = save_results("intel-scan", all_results)
    print(f"\nDone. {len(all_results)} unique items saved to {path}")
    return 0 if all_results else 1

if __name__ == "__main__":
    sys.exit(main())
