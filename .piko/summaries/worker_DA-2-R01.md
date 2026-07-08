# Worker Summary: DA-2-R01

## Round
- Round ID: DA-2-R01
- Round Name: Select Publish Candidates
- Stage: DA-2 Candidate Selection From Discovery
- Started from next_round: DA-2-R01

## Scope
- Allowed files touched: `packages/discovery/*`, `tests/test_discovery_search.py`, `.piko/summaries/worker_DA-2-R01.md`, `.piko/round_status.json`
- Files intentionally not touched: article pipeline runner, publishing paths, collectors, deployment config
- Upstream fixes made: none

## Changes
- Modified files: `packages/discovery/search_engine.py`, `packages/shared/schemas.py`, `tests/test_discovery_search.py`
- Added files: `.piko/summaries/worker_DA-2-R01.md`
- Deleted files: none
- Behavioral changes: added `select_publish_article_candidates`, which selects only runnable `publish_candidate` discovery clusters and returns candidate-only article candidate records.

## Selected And Excluded Examples
- Selected: `candidate_stardew_valley_save_file_location`, decision `publish_candidate`, runnable `true`, publish_ready `false`
- Excluded: Hades II crash watchlist candidate, decision `watchlist_waiting_for_answer`, runnable `false`
- Excluded: Stardew Valley save recovery risk candidate, decision `blocked_high_risk`, runnable `false`

## Task Status
- 执行任务: completed
- 测试任务: completed
- 协作验收任务: ready_for_verify

## Verification Run By Worker
- Commands run: `python -m pytest tests\test_discovery_search.py -q`
- Results: `21 passed in 0.63s`
- Failures: none

## Sample Output
```json
{
  "selected": {
    "candidate_id": "candidate_stardew_valley_save_file_location",
    "game_name": "Stardew Valley",
    "decision": "publish_candidate",
    "runnable": true,
    "publish_ready": false,
    "requires_evidence_pipeline": true
  },
  "excluded_decisions": [
    "watchlist_waiting_for_answer",
    "blocked_high_risk"
  ]
}
```

## Direction Check
- Player need: selection starts from discovery clusters.
- Source evidence: selected candidates preserve source hints, source regions, and source types.
- Structured judgment: selection requires `decision=publish_candidate`, `runnable=true`, `publish_ready=false`, and `requires_evidence_pipeline=true`.
- Clear guide output: no article generation is performed.
- Traceable sources: cluster id and query hints are carried forward.
- Risk warnings: watchlist and high-risk candidates are excluded from runnable selection.

## Prohibited Items Check
- Real external API: no
- Real crawler: no
- Real publishing: no
- Admin review / human approval: no
- Unsourced claims: no article claims generated

## Risks And Notes
- Unfinished: DA-3 will decide how selected candidates invoke the evidence pipeline.
- Risks: downstream code must not interpret selected/runnable as publish approval.
- Assumptions: `publish_ready=false` remains mandatory for discovery-selected candidates.

## Next Recommendation
- Suggested next round: DA-2-R02
- Why: selected candidates need source query hints for later evidence collection.
