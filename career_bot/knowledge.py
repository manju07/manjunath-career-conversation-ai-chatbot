import json
from html.parser import HTMLParser
from pathlib import Path

from pypdf import PdfReader

from career_bot.config import DATA_DIR, WEBSITE_DIR, website_repo_path

WEBSITE_SOURCES = (
    "Resume-Data.md",
    "Quote-Service-Project-Details.md",
    "README.md",
)


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        if tag in ("p", "h1", "h2", "h3", "h4", "li", "section"):
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip:
            return
        text = data.strip()
        if text:
            self.parts.append(text + " ")


def _pdf_text(path: Path) -> str:
    if not path.exists():
        return ""
    reader = PdfReader(str(path))
    chunks = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            chunks.append(text)
    return "\n".join(chunks)


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def _html_text(path: Path) -> str:
    parser = _TextExtractor()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    lines = []
    for raw in "".join(parser.parts).splitlines():
        line = " ".join(raw.split())
        if line:
            lines.append(line)
    return "\n".join(lines)


def _website_snapshot() -> str:
    sections = []
    for path in sorted(WEBSITE_DIR.glob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        body = _read(path).strip()
        if body:
            sections.append(f"### {path.name}\n{body}")
    return "\n\n".join(sections)


def _live_website() -> str:
    repo = website_repo_path()
    if repo is None:
        return ""
    sections = [f"Loaded from local repo: {repo}"]
    for name in WEBSITE_SOURCES:
        body = _read(repo / name).strip()
        if body:
            sections.append(f"### {name}\n{body}")
    for name in ("index.html", "blogs.html"):
        path = repo / name
        if path.exists():
            sections.append(f"### {name}\n{_html_text(path)}")
    return "\n\n".join(sections)


def load_profile() -> dict:
    courses_path = DATA_DIR / "courses.json"
    courses = json.loads(courses_path.read_text(encoding="utf-8")) if courses_path.exists() else []
    website = _live_website() or _website_snapshot()
    return {
        "summary": _read(DATA_DIR / "summary.txt"),
        "linkedin": _pdf_text(DATA_DIR / "Profile.pdf"),
        "resume": _pdf_text(DATA_DIR / "Manjunath_Asundi.pdf"),
        "courses": courses,
        "website": website,
    }
