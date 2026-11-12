# PK Quant Trading Firm — Independent Research Plan

This fork is an independent project based on the upstream Day Trader skill. It is a research and paper-trading workspace. Live order routing is disabled by default and is not part of the initial build milestone.

## Current baseline

- Fork: `https://github.com/prashantkumaromar/day-trader-skill`
- Upstream: `https://github.com/Jakeschincariol/day-trader-skill`
- Local project: `/Users/prashantkumar/Documents/PK Day Trader Skill`
- Python: 3.12.4
- Offline test result: 315 tests passed with:

  ```bash
  python3 -m unittest discover -s tests -p 'test_*.py' -v
  ```

- Note: the repository's README test command omits the filename pattern and currently discovers zero tests on this checkout. The explicit command above is the reproducible baseline.

## Research-first milestones

1. Preserve the upstream skill behavior and add a project-specific test harness.
2. Reproduce the built-in TSLA opening-range-breakout Time Machine example from offline fixtures.
3. Add a research manifest for every run: source, retrieval time, timezone, bar interval, plan, seed, costs, slippage, and limitations.
4. Backtest a small set of explicitly defined stock setups using historical data, with chronological splits and no leakage.
5. Compare simulated outcomes with realized historical setup outcomes; do not call either result a prediction.
6. Add paper-only portfolio state, reconciliation, and kill-switch tests.
7. Consider broker integration only after the research and paper gates pass. Any live mode must be opt-in, separately configured, approval-gated, and disabled in CI.

## First reproduced result

The repository's offline TSLA example was reproduced with seed 19, 10,000 replays, and 59 prior full sessions:

- Target first: 29.38%
- Stop first: 25.48%
- Neither by the close: 45.14%
- Green: 51.68%
- Average simulated R: +0.034
- Historical rule occurrences: 33
- Historical target / stop / close: 13 / 15 / 5
- Historical average R: -0.062

Interpretation: the repository labels this setup “close to a coin flip.” This is a reproducibility check, not evidence of an edge.

## Explicit boundaries

- No credentials in the repository or chat.
- No live broker connection in the initial milestones.
- No autonomous order placement.
- No options orders, leverage, shorting, or margin in the initial milestones.
- Every backtest result must retain its data and execution assumptions.
