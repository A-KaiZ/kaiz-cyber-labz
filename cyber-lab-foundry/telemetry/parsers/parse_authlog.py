"""Parse SSH authentication events into CSV."""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Iterable, Iterator

LOG_PATTERN = re.compile(
    r"^(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<host>\S+)\s+sshd\[\d+\]:\s+(?P<message>.*)$"
)
FAIL_PATTERN = re.compile(r"Failed password for (?P<user>\w+) from (?P<src>\d+\.\d+\.\d+\.\d+)")
SUCCESS_PATTERN = re.compile(r"Accepted password for (?P<user>\w+) from (?P<src>\d+\.\d+\.\d+\.\d+)")

MONTHS = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path, help="Path to auth.log")
    parser.add_argument("--output", type=Path, default=Path("auth_events.csv"), help="CSV output path")
    return parser


def parse_lines(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    for line in lines:
        match = LOG_PATTERN.match(line)
        if not match:
            continue
        message = match.group("message")
        for pattern, outcome in ((FAIL_PATTERN, "failure"), (SUCCESS_PATTERN, "success")):
            detail = pattern.search(message)
            if detail:
                yield {
                    "timestamp": f"2024-{MONTHS.get(match.group('month'), '01')}-{int(match.group('day')):02d} {match.group('time')}",
                    "host": match.group("host"),
                    "user": detail.group("user"),
                    "source_ip": detail.group("src"),
                    "outcome": outcome,
                }
                break


def run(args: argparse.Namespace) -> None:
    lines = args.log.read_text(encoding="utf-8").splitlines()
    events = list(parse_lines(lines))
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["timestamp", "host", "user", "source_ip", "outcome"])
        writer.writeheader()
        writer.writerows(events)
    print(f"Wrote {len(events)} events to {args.output}")


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
