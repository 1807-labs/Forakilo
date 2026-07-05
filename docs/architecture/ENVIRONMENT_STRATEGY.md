# Environment Strategy

Purpose: define separation between development, research, training, paper, and live environments.
Scope: environment boundaries and promotion rules.
Audience: engineers, ML engineers, operations, risk reviewers, and security reviewers.
Assumptions: environment confusion is a high-risk failure mode.
Dependencies: [Deployment Architecture](DEPLOYMENT_ARCHITECTURE.md), [Paper to Live Trading Gate](../trading/PAPER_TO_LIVE_TRADING_GATE.md).
Unresolved decisions: environment naming conventions and hosting accounts.

## Environments

| Environment | Purpose | Credentials | Trading capability |
| --- | --- | --- | --- |
| Local | Development and fixtures | Fake only by default | None |
| Research | Offline analysis | Data-provider research keys only | None |
| Training | Candidate model training | Dataset/artifact access | None |
| Paper | Simulated or sandbox trading | Sandbox/demo credentials | Paper/sandbox only |
| Staging | Release validation | Sandbox/demo credentials | Paper/sandbox only |
| Production | User-facing service | Live credentials only after approval | Disabled until gates pass |

## Separation Rules

- Sandbox and live credentials MUST be separated by environment and storage namespace.
- Paper and live UI states MUST use distinct labels and visual treatments.
- Research data MUST NOT leak into live inference without approved lineage and contract validation.
- Model artifacts MUST carry environment, code, data, feature, and approval metadata.
