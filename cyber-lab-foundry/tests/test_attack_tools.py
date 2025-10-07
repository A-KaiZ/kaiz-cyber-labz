from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pytest

from redteam.tools.brute_ssh import generate_candidates
from redteam.tools.sqli_probe import analyze


def test_generate_candidates_creates_defaults(tmp_path: Path) -> None:
    wordlist = tmp_path / "list.txt"
    candidates = generate_candidates(wordlist, "victim")
    assert "victim123" in candidates
    assert "WeakPass123!" in candidates
    assert wordlist.read_text(encoding="utf-8").strip() != ""


def test_analyze_marks_differences(monkeypatch: pytest.MonkeyPatch) -> None:
    responses: Iterator[str] = iter(["baseline", "different", "different", "baseline"])

    class _Resp:
        def __init__(self, content: str) -> None:
            self.text = content
            self.status_code = 200

    def fake_post(url: str, data: dict[str, str], timeout: int) -> _Resp:  # type: ignore[override]
        return _Resp(next(responses))

    monkeypatch.setattr("redteam.tools.sqli_probe.requests.post", fake_post)
    results = analyze("http://example", "' OR '1'='1", "baseline")
    assert any(result.is_different for result in results)
