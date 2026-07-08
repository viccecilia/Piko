# Worker Summary: RM-4-R02

## Round
- Round ID: RM-4-R02
- Round Name: Real Topic To Candidate Pilot
- Stage: RM-4
- Started from next_round: RM-4-R01

## Scope
- Allowed files touched: `packages/discovery/*`, `packages/workflows/*`, `artifacts/candidate_drafts/*`, `tests/test_discovery_search.py`, `.piko/summaries/worker_RM-4-R02.md`
- Files intentionally not touched: publishing, deployment, gates, LLM defaults
- Upstream fixes made: none

## Changes
- Modified files:
  - `tests/test_discovery_search.py`
- Added files:
  - `packages/discovery/real_market_pilot.py`
  - `artifacts/candidate_drafts/stardew-valley-save-file-location-candidate-stardew-valley-save-file-location.json`
  - `artifacts/candidate_drafts/stardew-valley-save-file-location-candidate-stardew-valley-save-file-location.md`
  - `.piko/summaries/worker_RM-4-R02.md`
- Deleted files: none
- Behavioral changes: Added `real_market_candidate_pilot()` to select a safe publish candidate, run existing internal candidate workflow, write internal draft artifacts, and show watchlist/high-risk blocks.

## Task Status
- Execution tasks: completed
- Test tasks: completed
- Collaboration acceptance tasks: Selected topic, candidate id, artifact path, and verification status listed below.

## Verification Run By Worker
- Commands run:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m packages.workflows.article_pipeline`
  - candidate artifact probe
- Results:
  - `62 passed in 2.35s`
  - article pipeline completed
  - Candidate pilot completed with internal artifact and preserved safety fields
- Failures: none

## Sample Output
```json
{
  "status": "completed",
  "candidate_id": "candidate_stardew_valley_save_file_location",
  "artifact_json": "artifacts\\candidate_drafts\\stardew-valley-save-file-location-candidate-stardew-valley-save-file-location.json",
  "verification_status": "fail",
  "publish_ready": false,
  "publishing_performed": false,
  "watchlist_runnable": false,
  "high_risk_runnable": false
}
```

## Direction Check
- Player need: Selected safe topic is Stardew Valley save file location.
- Source evidence: Candidate still must pass evidence pipeline and verification.
- Structured judgment: Candidate artifact includes verification report, safety fields, agent trace, sources, evidence cards, ranked steps.
- Clear guide output: Internal draft only, not public content.
- Traceable sources: Existing workflow source/evidence trace is preserved.
- Risk warnings: Verification status is recorded as `fail`; artifact remains blocked/internal.

## Prohibited Items Check
- Publishing: no
- Deploy: no
- Watchlist/high-risk normal draft: blocked
- Publish-ready output: no
- Verification weakened: no
- Default network/LLM: no

## Risks And Notes
- Unfinished: Candidate verification currently fails, so output remains blocked.
- Risks: Future pilot should investigate verification failure before using the candidate in later workflows.
- Assumptions: A mocked real-market equivalent is acceptable because no live endpoint is configured.

## Next Recommendation
- Suggested next round: RM-4-R03
- Why: Final docs, verification, and batch summary.
