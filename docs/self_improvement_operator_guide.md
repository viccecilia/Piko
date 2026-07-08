# Self-Improvement Operator Guide

Use the self-improvement API when a workflow or verification report shows a problem and you want structured next-step planning.

## Typical Flow

1. Run a workflow.
2. Verify the workflow result.
3. Send the verification or workflow report to an improvement endpoint.
4. Read the diagnostic report.
5. Review the upgrade proposal.
6. Review the patch plan.
7. Run or approve regression commands only after a worker implements an approved change.
8. Append a ledger entry if the proposal should be tracked.

## Ledger Safety

Ledger entries are for upgrade metadata only. They must not contain raw source bodies, credentials, tokens, authorization headers, passwords, API keys, or other secrets.

Before writing JSONL, the ledger helper rejects prohibited sensitive field names such as `raw_text`, `secret`, `password`, `api_key`, `authorization`, `access_token`, and `refresh_token`. Long strings are truncated and a guardrail warning is added to the entry notes.

If a ledger write fails because of a guardrail, remove the sensitive or raw field from the proposal context and keep only a short, source-linked summary.

## API Endpoints

- `POST /improvement/diagnose`
- `POST /improvement/propose`
- `POST /improvement/from-verification-report`
- `POST /improvement/from-workflow-report`

## Stop Conditions

Stop before implementation if a proposal would:

- Enable live connectors by default
- Publish or deploy
- Bypass verification
- Touch unrelated domains
- Store long raw source text
- Add human approval/Admin Review infrastructure
