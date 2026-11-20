"""Run: python scripts/test_fetch_trending.py  (no network needed)"""
from fetch_trending import looks_safe

base = {"full_name": "dev/tool", "description": "A useful CLI for developers", "license": {"spdx_id": "MIT"},
        "language": "Python", "fork": False, "archived": False, "open_issues_count": 3,
        "stargazers_count": 1000, "forks_count": 80}
assert looks_safe(base)
assert not looks_safe({**base, "forks_count": 0}), "star farm"
assert not looks_safe({**base, "description": "Windows LockScreen Bypass 0day"}), "exploit"
assert not looks_safe({**base, "description": ""}), "no description"
assert not looks_safe({**base, "language": None}), "no code"
assert not looks_safe({**base, "license": None}), "no licence"
assert not looks_safe({**base, "open_issues_count": 900}), "issue spam"
print("ok")
