---
name: User Story
about: Define a new user story and its acceptance criteria for forakilo
title: '[STORY] Historical backtesting and strategy validation module'
labels: user story, enhancement, backtesting
assignees: ''
---

## User Story
**As a** risk-conscious trader,
**I want** to run `forakilo` against historical data,
**So that** I can evaluate its profitability, drawdown, and robustness before risking live capital.

---

## Acceptance Criteria
- [ ] Generates a comprehensive performance report showing key metrics: Win Rate, Sharpe Ratio, Profit Factor, and Maximum Drawdown.
- [ ] Simulates realistic slippage based on market volatility and order book depth.
- [ ] Deducts accurate maker/taker exchange fees and forex spreads during the simulation.
- [ ] Outputs an equity curve graph or structured JSON summary at the end of the test run.

---

## Technical Notes / Constraints
* **Execution Mode:** Offline Backtest / Simulation
* **Dependencies:** `backtrader` or custom vectorized engine, `matplotlib` / `plotly` (for visual reporting)
