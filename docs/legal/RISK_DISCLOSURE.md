# Risk Disclosure Draft

This is a working technical draft for product planning and is not a substitute for qualified legal advice.

Purpose: draft risk disclosure principles for user-facing review.
Scope: cryptocurrency, FX, paper trading, backtesting, models, automation, and providers.
Audience: product owners, legal counsel, users, and reviewers.
Assumptions: final wording requires legal approval before publication.
Dependencies: [Product Classification](PRODUCT_CLASSIFICATION_AND_REGULATORY_ASSUMPTIONS.md), [Terms Draft](TERMS_OF_SERVICE_DRAFT.md).
Unresolved decisions: jurisdiction-specific mandated disclosures.

## Draft Disclosure Points

- Trading cryptocurrency, FX, CFDs, derivatives, or margin products can cause substantial loss.
- Paper trading and backtesting do not reproduce all live market conditions.
- Historical results do not prove future results.
- Models can be wrong, stale, overfit, miscalibrated, or unsuitable for current market regimes.
- Market data can be delayed, incomplete, revised, or inaccurate.
- Providers can reject, delay, partially fill, or cancel orders.
- Network, software, infrastructure, and provider failures can affect results.
- Forakilo does not provide personalized financial advice in the MVP.
- Users are responsible for understanding provider terms, fees, tax obligations, and risks.

## Acceptance Flow

Before enabling any provider connection or live gate, users SHOULD receive clear risk acknowledgement, non-advisory disclosure, provider-specific terms, and paper/live mode explanation.
