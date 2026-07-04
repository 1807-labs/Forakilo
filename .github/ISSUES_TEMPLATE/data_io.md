---
name: User Story
about: Define a new user story and its acceptance criteria for forakilo
title: '[STORY] Connect to major Crypto and Forex exchange APIs'
labels: user story, enhancement, data-ingestion
assignees: ''
---

## User Story
**As a** trader,
**I want** `forakilo` to connect to major crypto and forex exchange APIs (e.g., Binance, OANDA),
**So that** the bot can fetch real-time market data and execute orders seamlessly across multiple platforms.

---

## Acceptance Criteria
- [ ] Successfully fetches live price feeds via WebSockets with fallback to REST APIs.
- [ ] Authenticates securely using encrypted API keys stored in environment variables or a secrets manager.
- [ ] Handles connection drops gracefully by implementing automatic reconnection with exponential backoff.
- [ ] Normalizes data structures between different exchanges so downstream engines receive a unified format.

---

## Technical Notes / Constraints
* **Target Markets:** Crypto (Binance/Kraken) & Forex (OANDA/IG)
* **Dependencies:** `ccxt` (for crypto), `requests` / `websockets`, `python-dotenv` / `cryptography`
