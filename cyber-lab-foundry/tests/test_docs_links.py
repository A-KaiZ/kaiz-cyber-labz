from __future__ import annotations

import re
from pathlib import Path

DOC_PATHS = [Path("README.md")] + list(Path("docs").rglob("*.md"))
LINK_RE = re.compile(r"\[[^\]]+\]\((?!http)(?!mailto)([^)#]+)")


def extract_links(markdown: str) -> list[str]:
    return LINK_RE.findall(markdown)


def test_relative_links_exist() -> None:
    for doc in DOC_PATHS:
        content = doc.read_text(encoding="utf-8")
        for link in extract_links(content):
            target = (doc.parent / link).resolve()
            assert target.exists(), f"Broken link {link} in {doc}"
