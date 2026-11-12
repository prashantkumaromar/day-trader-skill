# SPY skill workflow

The independent fork now includes a reproducible five-stage runner:

```bash
python3 scripts/run_spy_workflow.py \
  --offline /path/to/SPY-chart.json.gz \
  --now "2026-10-19 10:15"
```

It runs:

1. `trader-scanner` — SPY 15-minute opening-range scan
2. `trader-entry` — entry status and trigger artifact
3. `trader-exit` — 1.5R target, opening-range-midpoint stop, 15:55 ET flat time
4. `trader-timemachine` — 10,000 replays with seed 19
5. `trader-risk` — only after a reviewed `trader/orders.json` exists

The runner requires `--now` so that historical results are reproducible. It
does not call `trader-broker` and cannot place an order. The risk stage is
intentionally blocked until position sizing creates an order file; this keeps
the research workflow separate from execution.

The configured local guardrails are paper-only, long stock/ETF only, no
options, no margin, no shorting, and a $25 maximum loss per trade.
