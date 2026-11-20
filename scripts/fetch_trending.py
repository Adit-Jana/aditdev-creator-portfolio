"""Write data/trending.json: the most-starred new GitHub repos of the past week, overall and AI-only.

Uses the public GitHub search API. Runs daily from .github/workflows/trending.yml;
set GITHUB_TOKEN for a higher rate limit (the workflow does this for you).

Raw "most starred this week" is full of star-farmed clones and hacking tools, so every
repo must pass `looks_safe` before it can appear on the site.
"""
import json, os, re, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "trending.json"
SHOW = 8
now = datetime.now(timezone.utc)
since = (now - timedelta(days=7)).strftime("%Y-%m-%d")

QUERIES = {
    "all": f"created:>{since}",
    "ai": f"llm OR agent OR claude OR mcp OR ai created:>{since}",
}
BLOCK = re.compile(
    r"bypass|0day|zero.?day|exploit|crack|keygen|cheat|aimbot|credential|password|stealer|grabber|"
    r"inject|spoof|unlock|activator|hwid|proxy|vpn|config.?checker|invite|register|free.?(robux|v.?bucks)|"
    r"gta|recomp|airdrop|wallet|crypto|token.?gen|loader|rat\b|botnet|ddos", re.I)

def looks_safe(i):
    desc = i.get("description") or ""
    text = f"{i['full_name']} {desc}"
    ascii_share = sum(c.isascii() for c in desc) / max(1, len(desc))
    return (desc and ascii_share > 0.9            # readable English description
            and i.get("license")                  # has an open-source licence
            and i.get("language")                 # real code, not a lone zip or README
            and not i["fork"] and not i["archived"]
            and i["open_issues_count"] < i["stargazers_count"] * 0.3   # issue spam
            and i["forks_count"] >= 15            # star farms have no forks
            and i["forks_count"] / max(1, i["stargazers_count"]) >= 0.02
            and not BLOCK.search(text))

def search(q):
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": q, "sort": "stars", "order": "desc", "per_page": 60})
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "trending-fetch"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        items = json.load(r)["items"]
    seen, out = set(), []
    for i in items:
        key = i["name"].lower()                    # drop clones that share a repo name
        if key in seen or not looks_safe(i):
            continue
        seen.add(key)
        out.append({"name": i["full_name"], "url": i["html_url"], "description": i["description"][:180],
                    "stars": i["stargazers_count"], "language": i["language"], "created": i["created_at"][:10]})
        if len(out) == SHOW:
            break
    return out

if __name__ == "__main__":
    data = {"updated": now.strftime("%Y-%m-%dT%H:%MZ"), "since": since, **{k: search(q) for k, q in QUERIES.items()}}
    assert data["all"], "no repositories passed the filter"
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}: {len(data['all'])} all, {len(data['ai'])} ai, since {since}")
