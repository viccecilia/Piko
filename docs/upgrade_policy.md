# Upgrade Policy

Piko upgrades must be traceable, reversible, and verified.

## Upgrade Proposal Requirements

Each proposal must include:

- Reason
- Affected modules
- Expected benefit
- Risk level
- Required tests
- Operator decision requirement

## Patch Plan Requirements

Patch plans describe intended edits only. They must not apply patches by themselves.

Each step should include:

- Target file
- Change summary
- Reason
- Verification method

## Approval Boundary

An operator or explicit worker instruction is required before code changes are implemented from an upgrade proposal.

## Ledger Guardrails

Upgrade ledger entries must stay small, reviewable, and free of secrets or raw source dumps.

Ledger writes reject payloads with field names containing:

- `raw_text`
- `credentials` or `credential`
- `secret`
- `password`
- `api_key`
- `authorization`
- `access_token`
- `refresh_token`

Long strings are truncated before JSONL write and the ledger entry receives a guardrail warning in `notes`. Do not use the ledger as raw source storage; store only proposal, plan, regression, and decision metadata.
