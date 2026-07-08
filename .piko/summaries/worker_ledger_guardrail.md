# Worker Summary: ledger-guardrail

## Round
- Round ID: ledger-guardrail
- Round Name: Ledger Guardrail Round
- Started from: self-improvement-stages verified passed

## Scope
- Allowed files touched:
  - `packages/improvement/upgrade_ledger.py`
  - `tests/test_self_improvement.py`
  - `docs/upgrade_policy.md`
  - `docs/self_improvement_operator_guide.md`
  - `.piko/summaries/worker_ledger_guardrail.md`
- Files intentionally not touched:
  - workflow publishing behavior
  - connector behavior
  - deployment scripts
  - crawler or source collection code

## Changes
- Added ledger guardrail checks before JSONL writes.
- Added `LedgerGuardrailError`.
- Added recursive prohibited field-name detection for:
  - `raw_text`
  - `credentials`
  - `credential`
  - `secret`
  - `password`
  - `api_key`
  - `authorization`
  - `access_token`
  - `refresh_token`
- Added long-string truncation at 2000 characters.
- Added ledger warning notes when truncation happens.
- Added tests for normal write, secret rejection, raw_text rejection, and long snippet truncation.
- Updated upgrade/operator docs to describe ledger safety rules.

## Verification Run By Worker
- Commands run:
  - `python -m pytest`
  - `python -m packages.workflows.article_pipeline`
  - prohibited-item scan with `rg`
- Results:
  - `python -m pytest`: 64 passed, 2 skipped in 0.87s.
  - `python -m packages.workflows.article_pipeline`: status=completed; real_collection_performed=False; verification_status=pass; publish_decision=verified_candidate.
  - Prohibited-item scan only found documentation warnings and existing policy text.
- Failures:
  - none

## Guardrail Behavior
```json
{
  "normal_ledger_write": "allowed",
  "secret_field": "rejected with LedgerGuardrailError",
  "raw_text_field": "rejected with LedgerGuardrailError",
  "long_snippet": {
    "action": "truncated",
    "limit": 2000,
    "warning_recorded_in_notes": true
  }
}
```

## Prohibited Items Check
- Workflow publishing behavior changed: no
- New API integration: no
- New crawler: no
- Deployment: no
- Automatic apply patch: no
- Git commit: no
- Tests deleted: no
- Default pytest network access: no; live smoke tests remain skipped by default

## Risks And Notes
- The guardrail checks field names and long strings in ledger payloads. It does not attempt semantic secret scanning inside arbitrary normal text.
- Sensitive field names are rejected rather than sanitized because writing secrets with renamed fields would be unsafe.
- Long strings are truncated with warning notes to keep ledger JSONL readable.

## Next Recommendation
- Piko-verify should inspect `append_ledger_entry`, guardrail tests, and the docs.
- Piko-verify should confirm ledger writes reject sensitive keys and that normal workflow/publishing behavior is unchanged.
