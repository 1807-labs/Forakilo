# Jurisdiction Research

This is a working technical draft for product planning and is not a substitute for qualified legal advice.

Purpose: record jurisdictional research assumptions.
Scope: Canada first; future multi-jurisdictional expansion.
Audience: legal counsel, product owners, risk reviewers, and engineers.
Assumptions: Canadian privacy, securities, derivatives, crypto, FX, and automated-trading obligations may apply depending on product model.
Dependencies: [Sources](../research/SOURCES.md), [Product Classification](PRODUCT_CLASSIFICATION_AND_REGULATORY_ASSUMPTIONS.md).
Unresolved decisions: province-by-province analysis, user eligibility, and provider availability.

## Canada Research Notes

- PIPEDA governs many private-sector commercial uses of personal information in Canada and requires accountability, consent, limiting collection/use/retention, safeguards, openness, access, and challenge mechanisms.
- Bill C-27 was a 44th Parliament bill and is not assumed to be in force for this baseline. Replacement privacy or AI legislation must be monitored.
- Canadian crypto asset trading platforms are regulated and the CSA maintains an authorized-platform list. Provider eligibility must be checked immediately before integration.
- CSA Staff Notices 21-332 and 21-333 show heightened regulatory expectations for crypto trading platforms and value-referenced crypto assets.
- NI 23-103 and CIRO electronic trading guidance indicate that automated order systems require risk and supervisory controls in applicable contexts.
- FX/CFD products can involve derivatives, margin, and dealer obligations. OANDA or any FX provider must be reviewed for account eligibility and product scope.

## Expansion Framework

Before adding a jurisdiction, Forakilo MUST assess privacy law, securities/derivatives law, crypto-asset rules, FX/CFD rules, marketing restrictions, data localization, tax reporting implications, provider availability, user eligibility, disclosures, complaint handling, and incident notification.
