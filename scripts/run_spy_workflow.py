#!/usr/bin/env python3
"""Run the SPY research workflow without placing orders.

The input is a saved Yahoo-compatible chart JSON/JSON.GZ file. The five skill
stages write their normal artifacts under trader/. The runner refuses to use
the current clock unless --now is supplied, making historical runs repeatable.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(label: str, args: list[str]) -> None:
    print(f"\n=== {label} ===")
    print("$", " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", type=Path, required=True,
                        help="saved SPY chart JSON or JSON.GZ")
    parser.add_argument("--now", required=True,
                        help='historical New York time, e.g. "2026-10-19 10:15"')
    parser.add_argument("--entry-setup", choices=["orb", "level"], default="orb")
    args = parser.parse_args()

    offline = str(args.offline.expanduser().resolve())
    common = ["--offline", offline, "--now", args.now, "--config", "trader/config.json"]

    run("1. trader-scanner", [
        sys.executable, "trader-scanner/scan.py", "orb", "--symbols", "SPY",
        "--or-minutes", "15", "--out", "trader/watchlist.json", *common,
        "--json",
    ])
    run("2. trader-entry", [
        sys.executable, "trader-entry/entry.py", "check", "SPY",
        "--setup", args.entry_setup, "--interval", "5m", "--write",
        "trader/entry.json", *common, "--json",
    ])
    run("3. trader-exit", [
        sys.executable, "trader-exit/exit.py", "plan", "--from",
        "trader/entry.json", "--stop", "or-mid", "--target", "1.5R",
        "--flat-by", "15:55", "--write", "trader/plan.json", *common,
        "--json",
    ])
    run("4. trader-timemachine", [
        sys.executable, "trader-timemachine/timemachine.py", "run",
        "--offline", offline, "--now", args.now, "--replays", "10000",
        "--seed", "19", "--write", "trader/timemachine.json", "--json",
    ])

    orders = ROOT / "trader/orders.json"
    if not orders.exists():
        print("\n=== 5. trader-risk ===")
        print("NOT RUN: trader/orders.json is missing. Run trader-budget after reviewing the plan and Time Machine output.")
        return 2
    run("5. trader-risk", [
        sys.executable, "trader-risk/check.py", "--orders", "trader/orders.json",
        "--config", "trader/config.json", "--now", args.now, "--json",
    ])
    print("\nWorkflow complete. No broker or order tool was called.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
