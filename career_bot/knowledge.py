import json
from html.parser import HTMLParser
from pathlib import Path

import requests
from pypdf import PdfReader

from career_bot.config import DATA_DIR, LINKS, WEBSITE_DIR, website_repo_path

SKIP_DIRS = {".git", ".qodo", "vendor", "css", "scss", "javascripts", "images", "vedanth-birthday"}
# Older resume copies still say "8+ years" and disagree with the current site.
SKIP_FILES = {
    "Manjunath_Asundi.pdf",
    "Manjunath_Asundi_Attractive_Resume_2024.pdf",
    "Manjunath_Asundi_Resume_2024.pdf",
}
TEXT_SUFFIXES = {".md", ".txt", ".html", ".htm"}
LIVE_PATHS = (
    "",
    "blogs.html",
    "README.md",
    "Resume-Data.md",
    "Quote-Service-Project-Details.md",
    "manjunath/summary.txt",
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
        if tag in ("p", "h1", "h2", "h3", "h4", "li", "section", "tr"):
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip:
            return
        text = " ".join(data.split())
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


def html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    lines = []
    for raw in "".join(parser.parts).splitlines():
        line = " ".join(raw.split())
        if line:
            lines.append(line)
    return "\n".join(lines)


def _file_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return _pdf_text(path)
    if path.suffix.lower() in {".html", ".htm"}:
        return html_to_text(_read(path))
    return _read(path)


def _repo_sections(repo: Path) -> list[str]:
    sections = [f"Local git repo: {repo}"]
    files = []
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES | {".pdf"}:
            continue
        if path.name in SKIP_FILES:
            continue
        files.append(path)
    for path in sorted(files):
        body = _file_text(path).strip()
        if body:
            sections.append(f"### repo:{path.relative_to(repo)}\n{body}")
    return sections


def _published_sections() -> list[str]:
    sections = [f"Published site: {LINKS['website']}"]
    for relative in LIVE_PATHS:
        url = LINKS["website"] + relative
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
        except requests.RequestException as exc:
            sections.append(f"### site:{relative or 'index.html'}\n(unavailable: {exc})")
            continue
        body = response.text
        if url.endswith(".html") or relative == "":
            body = html_to_text(body)
        body = body.strip()
        if body:
            sections.append(f"### site:{relative or 'index.html'}\n{body}")
    return sections


def _snapshot_sections() -> list[str]:
    sections = []
    if not WEBSITE_DIR.exists():
        return sections
    for path in sorted(WEBSITE_DIR.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
            body = _read(path).strip()
            if body:
                sections.append(f"### snapshot:{path.relative_to(WEBSITE_DIR)}\n{body}")
    return sections


def load_profile() -> dict:
    courses_path = DATA_DIR / "courses.json"
    courses = json.loads(courses_path.read_text(encoding="utf-8")) if courses_path.exists() else []

    sections = []
    seen = set()

    def add(section: str) -> None:
        body = section.split("\n", 1)[-1].strip()
        if not body or body in seen:
            return
        seen.add(body)
        sections.append(section)

    repo = website_repo_path()
    if repo is not None:
        for section in _repo_sections(repo):
            add(section)
    for section in _published_sections():
        add(section)
    if len(sections) <= 1:
        for section in _snapshot_sections():
            add(section)

    return {
        "summary": _read(DATA_DIR / "summary.txt"),
        "linkedin": _pdf_text(DATA_DIR / "Profile.pdf"),
        "resume": _pdf_text(DATA_DIR / "Manjunath_Asundi.pdf"),
        "courses": courses,
        "website": "\n\n".join(sections),
    }
