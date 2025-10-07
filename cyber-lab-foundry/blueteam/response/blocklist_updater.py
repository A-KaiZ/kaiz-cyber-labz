"""Manage simple iptables blocklist entries within the lab network."""
from __future__ import annotations

import argparse
import subprocess
from typing import Iterable


def run_command(command: list[str]) -> None:
    subprocess.run(command, check=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--block", help="Add IP address to DROP list")
    parser.add_argument("--unblock", help="Remove IP address from DROP list")
    parser.add_argument(
        "--chain",
        default="LABBLOCK",
        help="iptables chain name to manage (default: LABBLOCK)",
    )
    return parser


def ensure_chain(chain: str) -> None:
    existing = subprocess.run(["iptables", "-S", chain], capture_output=True, text=True)
    if existing.returncode != 0:
        run_command(["iptables", "-N", chain])
        run_command(["iptables", "-I", "INPUT", "-j", chain])


def block_ip(chain: str, ip: str) -> None:
    ensure_chain(chain)
    run_command(["iptables", "-A", chain, "-s", ip, "-j", "DROP"])


def unblock_ip(chain: str, ip: str) -> None:
    run_command(["iptables", "-D", chain, "-s", ip, "-j", "DROP"])


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    if not args.block and not args.unblock:
        parser.print_help()
        return 1
    if args.block:
        block_ip(args.chain, args.block)
    if args.unblock:
        unblock_ip(args.chain, args.unblock)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
