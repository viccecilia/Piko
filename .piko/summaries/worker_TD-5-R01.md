# Worker Summary: TD-5-R01

## Round
- Round ID: TD-5-R01
- Round Name: Watchlist State Machine
- Stage: TD-5 Watchlist Monitoring Logic
- Started from next_round: TD-5-R01

## Scope
- Allowed files touched: `packages/shared/schemas.py`, `packages/discovery/*`, `tests/test_discovery_search.py`, `.piko/summaries/worker_TD-5-R01.md`, `.piko/round_status.json`
- Files intentionally not touched: Redis/Celery scheduling, real source collectors, article generation, publishing paths, deployment config
- Upstream fixes made: none

## Changes
- Modified files: `packages/shared/schemas.py`, `packages/discovery/search_engine.py`, `tests/test_discovery_search.py`, `docs/player_pain_discovery.md`
- Added files: `.piko/summaries/worker_TD-5-R01.md`
- Deleted files: none
- Behavioral changes: `DiscoveryWatchlistItem` now has explicit `state`, `promotion_triggers`, and `state_transitions`; promotion output includes previous and next state.

## State Transitions
- `watching` -> `answer_seen` when accepted/official answer appears but evidence is not mature enough.
- `watching` -> `evidence_ready` when accepted/official/high-quality evidence is ready for pipeline review.
- `watching` -> `stale` when freshness and heat fade.
- `evidence_ready` -> `closed` only after handoff or dismissal; no auto-draft is generated.

## Task Status
- 执行任务: completed
- 测试任务: completed
- 协作验收任务: ready_for_verify

## Verification Run By Worker
- Commands run: `python -m pytest tests\test_discovery_search.py -q`
- Results: `35 passed in 0.66s`
- Failures: none

## Sample Output
```json
{
  "watchlist_id": "watch_hades_ii_crash_after_update",
  "state": "watching",
  "promotion_triggers": [
    "accepted_answer",
    "official_answer",
    "evidence_quality>=60"
  ],
  "publish_ready": false,
  "requires_evidence_pipeline": true
}
```

## Direction Check
- Player need: watchlist tracks a concrete unresolved player issue.
- Source evidence: accepted/official/evidence-quality signals are state triggers only.
- Structured judgment: state and transition map are explicit.
- Clear guide output: no guide or draft is generated.
- Traceable sources: last seen source regions and cluster id remain attached.
- Risk warnings: watchlist promotion never means publish-ready.

## Prohibited Items Check
- Real polling: no
- Redis/Celery scheduling: no
- Real external API: no
- Real crawler: no
- Real publishing: no
- Auto-generate drafts from watchlist: no

## Risks And Notes
- Unfinished: future real monitoring must be explicit opt-in and offline tests must remain default.
- Risks: state transitions are deterministic and may need operator tuning later.
- Assumptions: evidence_ready means candidate can be reviewed by evidence pipeline, not published.

## Next Recommendation
- Suggested next round: TD-5-R02
- Why: watchlist items need refresh interval recommendations without background execution.
