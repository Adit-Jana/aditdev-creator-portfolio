"""Render every guide in guides/src/*.html to guides/<name>.pdf with headless Chrome.

Usage:  python guides/build.py            (Chrome path auto-detected on Windows/macOS/Linux)
        CHROME=/path/to/chrome python guides/build.py
"""
import os, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATES = [
    os.environ.get("CHROME"),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chrome"),
]
chrome = next((c for c in CANDIDATES if c and Path(c).exists()), None)
if not chrome:
    sys.exit("Chrome not found. Set the CHROME environment variable to its path.")

for src in sorted((HERE / "src").glob("*.html")):
    out = HERE / f"{src.stem}.pdf"
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", f"--print-to-pdf={out}", src.as_uri()],
                   check=True, capture_output=True)
    assert out.exists() and out.stat().st_size > 10_000, f"{out.name} looks empty"
    print(f"{out.name}  {out.stat().st_size // 1024} KB")
