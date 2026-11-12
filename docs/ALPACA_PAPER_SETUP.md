# Alpaca paper-trading setup

Run this from the project directory:

```bash
python3 scripts/configure_alpaca_paper.py
```

The script securely prompts for the Alpaca **paper** API key and secret, then
updates Claude Desktop's configuration at:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

It preserves unrelated MCP servers, creates a local backup, writes the file
with owner-only permissions, and sets `ALPACA_PAPER_TRADE=true`. Restart Claude
Desktop after the script completes.

For a validation-only run without writing:

```bash
python3 scripts/configure_alpaca_paper.py --dry-run
```

Never paste credentials into chat, source files, GitHub, or command-line
arguments. The script does not verify paper mode from the account response;
paper mode is established by the configured paper keys and the explicit
`ALPACA_PAPER_TRADE=true` setting.
