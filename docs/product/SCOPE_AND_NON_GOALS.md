# Scope and Non-Goals

Purpose: define what Forakilo will and will not do in early releases.
Scope: foundation, MVP, controlled beta, and post-MVP boundaries.
Audience: product owners, engineers, legal counsel, and reviewers.
Assumptions: reducing custody, advice, leverage, and automation risk is necessary for a safe first product.
Dependencies: [Product Vision](PRODUCT_VISION.md), [Product Classification](../legal/PRODUCT_CLASSIFICATION_AND_REGULATORY_ASSUMPTIONS.md).
Unresolved decisions: whether Forakilo ever expands beyond user-authorized third-party execution.

## In Scope for Foundation

- Repository standards, documentation, secure SDLC, CI strategy, and issue templates.
- Authentication design, credential-security design, data contracts, and audit architecture.
- Provider research and technology decisions.

## In Scope for MVP

- Authenticated user registration and login.
- Approved sandbox/demo provider connection.
- Validated market data ingestion.
- Dashboard for global status, portfolio, trading, market intelligence, model operations, risk, audit, and operations.
- One approved strategy or baseline model.
- Auditable signals with expiry and confidence metadata.
- Deterministic pre-trade risk controls.
- Paper or sandbox order execution and reconciliation.
- Candidate retraining trigger, evaluation report, and shadow or paper deployment.
- Manual kill switch.

## Controlled Beta Scope

- Limited live trading only after gates pass.
- One approved venue or broker.
- Limited instruments, capital, exposure, and order types.
- Manual model promotion.
- Production security review, monitoring, incident response, rollback, and user risk acknowledgement.

## Non-Goals

- Custody of user fiat or cryptocurrency.
- Deposits, withdrawals, pooling of funds, or money transmission.
- Personalized financial advice.
- Social, mirror, or copy trading in the MVP.
- Unrestricted live trading.
- Autonomous live model promotion in MVP or initial live releases.
- General-purpose hosted LLMs in the market, risk, or execution path.
- Website scraping unless explicitly approved under provider terms and legal review.
- Ultra-low-latency market-making claims.
