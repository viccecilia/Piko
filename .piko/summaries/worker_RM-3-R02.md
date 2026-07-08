# Worker Summary: RM-3-R02

## Round
- Round ID: RM-3-R02
- Round Name: Hot Question And Guide Need Ranking
- Stage: RM-3
- Started from next_round: RM-3-R01

## Scope
- Allowed files touched: `packages/discovery/*`, `apps/api/routes/discovery.py`, `tests/test_discovery_search.py`, `.piko/summaries/worker_RM-3-R02.md`
- Files intentionally not touched: publishing workflow, article generation, evidence gates, real connectors, LLM adapters
- Upstream fixes made: none

## Changes
- Modified files:
  - `packages/discovery/rankings.py`
  - `tests/test_discovery_search.py`
- Added files:
  - `.piko/summaries/worker_RM-3-R02.md`
- Deleted files: none
- Behavioral changes: Added `rank_hot_question_buckets()` and `question_ranking_buckets` with answered, watchlist, conflict, high-risk, and must-check buckets.

## Task Status
- Execution tasks: completed
- Test tasks: completed
- Collaboration acceptance tasks: Sample buckets and one watchlist example included below.

## Verification Run By Worker
- Commands run:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m pytest`
  - API probe `/discovery/rankings?limit=5`
- Results:
  - `59 passed in 2.86s`
  - `139 passed, 3 skipped in 2.96s`
  - Ranking buckets present: answered, watchlist, conflict, high-risk, must-check
- Failures: none

## Sample Ranking Buckets
```json
{
  "hot_answered_questions": 5,
  "hot_unanswered_watchlist_questions": 1,
  "conflict_answer_topics": 1,
  "high_risk_blocked_topics": 1,
  "must_check_guide_topics": 3,
  "watchlist_example": {
    "game_name": "Hades II",
    "decision": "watchlist_waiting_for_answer",
    "runnable": false,
    "publish_ready": false
  }
}
```

## Direction Check
- Player need: Hot questions are split by answer maturity, conflict value, watchlist value, and risk.
- Source evidence: Derived from normalized topic clusters.
- Structured judgment: Each topic includes decision, intent, evidence quality, heat, answer status, risk, and next action.
- Clear guide output: Not generated.
- Traceable sources: Cluster source fields remain in the underlying discovery response.
- Risk warnings: High-risk topics are blocked and watchlist topics are non-runnable.

## Prohibited Items Check
- Auto article drafts: no
- Evidence pipeline bypass: no
- Publish-ready discovery output: no
- Default network: no
- Real crawler: no
- Publishing/deploy: no
- Default LLM: no

## Risks And Notes
- Unfinished: Buckets are heuristic and should be reviewed against live pilot data in RM-4.
- Risks: `must_check_guide_topics` is a prioritization signal only, not approval to draft or publish.
- Assumptions: `recommended_next_action` remains the authority for whether a cluster can move toward evidence pipeline work.

## Next Recommendation
- Suggested next round: RM-3-R03
- Why: Expose rankings in the discovery client/API surface.
