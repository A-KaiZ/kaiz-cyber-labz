from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Iterable

import requests

FILES = {
    "lab-auth": Path("/opt/telemetry/logs/victim-ssh/auth.log"),
    "lab-web": Path("/opt/telemetry/logs/victim-web/app.log"),
}
API_URL = "http://localhost:9200"


def tail_file(path: Path, seen: int) -> tuple[list[str], int]:
    if not path.exists():
        return [], seen
    data = path.read_text(encoding="utf-8")
    lines = data.splitlines()
    if len(lines) <= seen:
        return [], len(lines)
    return lines[seen:], len(lines)


def bulk_payload(index: str, lines: Iterable[str]) -> str:
    payload = []
    for line in lines:
        payload.append(json.dumps({"index": {"_index": index}}))
        payload.append(json.dumps({"message": line}))
    return "\n".join(payload) + ("\n" if payload else "")


def main() -> None:
    positions = {name: 0 for name in FILES}
    while True:
        for index, path in FILES.items():
            lines, new_pos = tail_file(path, positions[index])
            positions[index] = new_pos
            if not lines:
                continue
            data = bulk_payload(index, lines)
            try:
                requests.post(f"{API_URL}/_bulk", data=data, headers={"Content-Type": "application/x-ndjson"}, timeout=10)
            except requests.exceptions.RequestException:
                pass
        time.sleep(5)


if __name__ == "__main__":
    main()
