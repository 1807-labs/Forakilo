---
name: User Story
about: Define a new user story and its acceptance criteria for forakilo
title: '[STORY] Automated risk management and position sizing protocols'
labels: user story, enhancement, risk-management
assignees: ''
---

## User Story
**As a** user running an automated system,
**I want** `forakilo` to automatically attach stop-loss and take-profit orders to every trade,
**So that** my account balance is protected from sudden market volatility and black swan events.

---

## Acceptance Criteria
- [ ] Automatically calculates precise position sizing based on a fixed percentage of current total balance (e.g., risk strictly 1% per trade).
- [ ] Executes risk-mitigation orders (Stop-Loss and Take-Profit) instantly alongside the primary entry order using exchange OCO (One-Cancels-the-Other) orders where supported.
- [ ] Prevents new order execution if account margin drops below a predefined safety threshold.

---

## Technical Notes / Constraints
* **Target Markets:** Both Crypto & Forex (must account for distinct lot sizing rules in Forex vs. fractional units in Crypto)
* **API Constraints:** Must verify exchange support for native OCO or trailing stop orders.
