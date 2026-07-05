# ADR-0003: Dashboard Stack

Status: Accepted
Date: 2026-07-04

Purpose: select the frontend technology baseline.
Scope: authenticated dashboard and operator views.
Audience: frontend engineers, product designers, and accessibility reviewers.
Assumptions: dashboard users need dense, accurate status information rather than marketing pages.
Dependencies: [Dashboard Specification](../../product/DASHBOARD_SPECIFICATION.md), [Technology Evaluation](../../research/TECHNOLOGY_EVALUATION.md).
Unresolved decisions: deployment target and UI component packaging remain open.

## Decision

Use Next.js, TypeScript, React, Tailwind CSS, accessible Radix/shadcn-style primitives, TanStack Query, and Apache ECharts.

## Rationale

The dashboard needs typed interfaces, accessible controls, real-time status updates, and financial charting. The selected stack keeps most UI logic locally controlled and avoids vendor-only charting dependencies.

## Consequences

- Dashboard MUST meet WCAG 2.2 AA as the implementation target.
- Paper and live modes MUST be visually impossible to confuse.
- Trading controls MUST avoid manipulative profit-focused design.

## Alternatives Rejected

- TradingView widgets as default: rejected until licensing and redistribution terms are approved.
- Custom charting from scratch: rejected for MVP because chart correctness and accessibility would take focus from safety controls.
