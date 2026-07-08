# Worker Summary: REV-5-R02

## Round
- Round ID: REV-5-R02
- Round Name: Solution Source Hints And Evidence Readiness
- Stage: REV-5
- Started from next_round: REV-3-R01

## Changes
- Added `source_hints_and_evidence_readiness`.
- Produces source query hints, solution candidate signals, and evidence readiness preview.
- Marks needs page-level evidence, source trace, and evidence cards before publication.

## Verification Run By Worker
- Commands run: `python -m pytest tests\test_discovery_search.py tests\test_rev_batch_3_6.py -q`
- Results: 75 passed
- Failures: none

## Sample Output
```json
{"needs_page_level_evidence":true,"needs_source_trace":true,"publish_ready":false}
```

## Prohibited Items Check
- No real publishing, no full source retention, no unverified solution claim, no LLM.

## Risks And Notes
- Hints are handoff metadata only.
- Next: REV-5-R03.
