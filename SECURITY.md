# Security Policy

Purpose: explain how to report security issues for Forakilo.
Scope: vulnerability reporting, sensitive disclosures, and current security status.
Audience: users, researchers, maintainers, and security reviewers.
Assumptions: Forakilo is pre-development and has no production service.
Dependencies: [Threat Model](docs/security/THREAT_MODEL.md), [Secure SDLC](docs/security/SECURE_SDLC.md).
Unresolved decisions: private security advisory process and contact address must be configured by the repository owner.

## Current Status

Forakilo is pre-development. No production application, live trading integration, or hosted service is verified in this repository.

## Reporting

Do not disclose suspected vulnerabilities through public issues if they include exploit details, secrets, personal data, provider credentials, or trading-impacting behavior.

Until a private GitHub Security Advisory workflow or dedicated security contact is configured, report sensitive concerns directly to the repository owner through an established private channel.

## Supported Versions

No released versions are currently supported.

## Security Expectations

Forakilo will require authentication, least privilege, encrypted provider credentials, no withdrawal permissions, deterministic risk controls, audit trails, dependency scanning, secret scanning, SBOMs, and controlled release gates before any live trading capability is considered.
