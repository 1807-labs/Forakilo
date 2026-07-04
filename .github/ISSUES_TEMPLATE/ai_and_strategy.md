---
name: User Story
about: Define a new user story and its acceptance criteria for forakilo
title: '[STORY] Historical data ingestion and AI signal generation pipeline'
labels: user story, enhancement, ai-engine
assignees: ''
---

## User Story
**As a** quantitative developer,
**I want** to feed historical market data into the AI model,
**So that** `forakilo` can train on past price action and identify high-probability entry and exit signals.

---

## Acceptance Criteria
- [ ] Technical features (like MACD, RSI, ATR, and custom price embeddings) are generated cleanly from raw OHLCV price data.
- [ ] The model successfully processes historical feature pipelines without data leakage (look-ahead bias).
- [ ] The engine outputs unambiguous `BUY`, `SELL`, or `HOLD` signals tied to a configurable confidence threshold (e.g., trigger trade only if confidence > 75%).

---

## Technical Notes / Constraints
* **Target Markets:** Multi-asset (Forex & Crypto feature normalization required)
* **Dependencies:** `pandas`, `numpy`, `ta-lib` or `pandas_ta`, `PyTorch` / `scikit-learn`
