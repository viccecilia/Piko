# Piko Template Architecture

Piko is organized as a reusable multi-agent collaboration template plus a first domain implementation: source-based game guides.

## Piko Core

Piko Core is the reusable system layer:

- Agent Registry and Tool Registry
- Workflow orchestration
- Gate and verification contracts
- Structured memory interfaces
- Source/evidence traceability contracts
- Improvement diagnostics, proposals, patch plans, regression plans, and ledger records

Core code should not contain game-specific editorial assumptions unless the behavior is part of the general source-backed workflow contract.

## Domain Implementation

The current domain is Game Guide. It owns:

- Player need taxonomy
- Game/source-specific source types
- Article template and guide style
- Risk rules for game troubleshooting
- PCGamingWiki/MediaWiki pilot connector policy

Future domains can reuse Piko Core by providing their own source policy, evidence extraction rules, content template, gates, and domain adapter.

## Shared vs Domain

Shared core:

- `packages/shared`
- `packages/workflows`
- `packages/gates`
- `packages/memory`
- `packages/improvement`

Game guide domain:

- Game-specific collectors
- Game source fixture rules
- Game article template
- Game risk and publishing policy details

The current package names are still game-guide oriented in places. Future migration should move game-specific source and article behavior behind a domain adapter without changing the core verification contract.

