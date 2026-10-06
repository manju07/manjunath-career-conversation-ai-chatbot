import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
WEBSITE_DIR = DATA_DIR / "website"

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

NAME = "Manjunath Asundi"
LINKS = {
    "github": "https://github.com/manju07",
    "linkedin": "https://www.linkedin.com/in/manju07/",
    "website": "https://manju07.github.io/",
    "blogs": "https://manju07.github.io/blogs.html",
    "hackerrank": "https://www.hackerrank.com/profile/manju07",
    "email": "manjunathasundi07@gmail.com",
}


def website_repo_path() -> Path | None:
    configured = os.getenv("WEBSITE_REPO")
    candidates = []
    if configured:
        candidates.append(Path(configured))
    candidates.append(ROOT.parent / "manju07.github.io")
    for path in candidates:
        if path.is_dir() and (path / "index.html").exists():
            return path
    return None
