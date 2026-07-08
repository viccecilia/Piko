# Domain Adapter Contract

A Piko domain adapter defines how one content domain plugs into the reusable core.

## Required Capabilities

- Convert a user need into a normalized workflow request.
- Provide source candidate selection rules.
- Normalize source records into `SourceReference`.
- Extract evidence cards with traceable `source_id` values.
- Produce ranked steps only when evidence supports answer-level claims.
- Provide domain gates and risk notes.
- Provide article or answer templates.
- Provide verification expectations and regression examples.

## Core Interfaces Reused

- Agent Registry
- Tool Registry
- Workflow reports
- Gate results
- Verification reports
- Memory records
- Improvement reports

## Safety Requirements

- No domain adapter may publish, deploy, or enable live connectors by default.
- No adapter may pass long raw source bodies through every agent.
- No adapter may create player-facing claims without source traceability.
- No adapter may bypass verification.

