#!/usr/bin/env python3
"""Configure Alpaca's official MCP server for paper trading.

Secrets are entered through hidden prompts, written only to the local Claude
Desktop configuration, and never printed. Existing configuration is preserved
and backed up before replacement.
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import shutil
import stat
import sys
import tempfile
from getpass import getpass
from pathlib import Path


DEFAULT_CONFIG = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG,
                        help="Claude Desktop config path (default: %(default)s)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate and show the destination without writing")
    return parser.parse_args()


def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Config is not valid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit("Claude Desktop config must contain a JSON object at the top level.")
    return value


def write_secure_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_name(f"{path.name}.bak-{secrets.token_hex(4)}")
        shutil.copy2(path, backup)
        os.chmod(backup, stat.S_IRUSR | stat.S_IWUSR)
        print(f"Backup created: {backup}")

    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(fd, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(fd, "w") as handle:
            json.dump(value, handle, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    args = parse_args()
    api_key = getpass("Alpaca PAPER API key: ").strip()
    secret_key = getpass("Alpaca PAPER secret key: ").strip()
    if not api_key or not secret_key:
        raise SystemExit("Both paper credentials are required.")

    config = load_config(args.config)
    servers = config.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        raise SystemExit("The existing 'mcpServers' value must be a JSON object.")

    servers["alpaca-paper"] = {
        "command": "uvx",
        "args": ["alpaca-mcp-server"],
        "env": {
            "ALPACA_API_KEY": api_key,
            "ALPACA_SECRET_KEY": secret_key,
            "ALPACA_PAPER_TRADE": "true",
            "ALPACA_TOOLSETS": "account,stock-data,trading,assets,news",
        },
    }

    if args.dry_run:
        print(f"Validated paper configuration for: {args.config}")
        return 0

    write_secure_json(args.config, config)
    print(f"Configured Alpaca paper trading in: {args.config}")
    print("Restart Claude Desktop before using the Alpaca tools.")
    print("The credentials were not displayed, logged, or committed by this script.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nCancelled; no configuration was changed.", file=sys.stderr)
        raise SystemExit(130)
