# Worker Summary: REV-1-R03

## Round
- Round ID: REV-1-R03
- Round Name: Endpoint Verification CLI
- Stage: REV-1
- Started from next_round: REV-1-R01

## Scope
- Allowed files touched: `packages/discovery/*`, `tests/test_discovery_search.py`, `.piko/summaries/worker_REV-1-R03.md`, `.piko/summaries/worker_REV-1.md`, `.piko/round_status.json`
- Files intentionally not touched: live collection defaults, publishing, deployment, gates, REV-2 files
- Upstream fixes made: none

## Changes
- Modified files:
  - `tests/test_discovery_search.py`
- Added files:
  - `packages/discovery/real_endpoint_verify.py`
  - `.piko/summaries/worker_REV-1-R03.md`
- Deleted files: none
- Behavioral changes: Added `python -m packages.discovery.real_endpoint_verify --fixture`; live mode skips without opt-in or URL.

## Task Status
- Execution tasks: completed
- Test tasks: completed
- Collaboration acceptance tasks: CLI commands and sample outputs included below.

## Verification Run By Worker
- Commands run:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m pytest`
  - `python -m packages.discovery.real_endpoint_verify --fixture`
  - `python -m packages.discovery.real_endpoint_verify --live`
  - opt-in without `PIKO_APPROVED_ENDPOINT_URL` live skip probe
- Results:
  - `65 passed in 2.76s`
  - `145 passed, 3 skipped in 4.26s`
  - Fixture CLI: `status=passed`, 2 games, 4 questions
  - Live CLI without opt-in: `status=skipped`
  - Live CLI with opt-in but no URL: `status=skipped`
- Failures: none

## CLI Commands
```powershell
python -m packages.discovery.real_endpoint_verify --fixture
python -m packages.discovery.real_endpoint_verify --live
```

## Sample Fixture Output
```json
{
  "status": "passed",
  "mode": "fixture",
  "source_count": 1,
  "normalized_game_count": 2,
  "normalized_question_count": 4,
  "ranking_count": 2,
  "real_collection_performed": false,
  "publishing_performed": false
}
```

## Sample Live Skip Output
```json
{
  "status": "skipped",
  "mode": "live",
  "skipped_reason": "Live endpoint verification requires PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true and PIKO_LIVE_DISCOVERY_TEST=true.",
  "real_collection_performed": false,
  "publishing_performed": false
}
```

## Direction Check
- Player need: CLI verifies endpoint payloads before live use.
- Source evidence: Fixture normalizes to safe source records.
- Structured judgment: CLI outputs JSON with counts, retained fields, skip reason, and safety flags.
- Clear guide output: Not generated.
- Traceable sources: Source metadata is reported.
- Risk warnings: Live mode cannot silently run without opt-in and URL.

## Prohibited Items Check
- Live default: no
- Full response body storage: no
- REV-2 entered: no
- Publishing/deploy/LLM/translation: no

## Risks And Notes
- Unfinished: No actual approved URL verified.
- Risks: Future REV-2 live smoke must use this CLI with opt-in and approved URL.
- Assumptions: `PIKO_APPROVED_ENDPOINT_URL` will be the operator-provided endpoint env var.

## Next Recommendation
- Suggested next round: REV-2-R01
- Why: REV-1 is ready for Piko-verify; live endpoint smoke belongs to REV-2.
