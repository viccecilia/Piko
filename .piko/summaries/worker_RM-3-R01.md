# Worker Summary: RM-3-R01

## Round
- Round ID: RM-3-R01
- Round Name: Real Market Hot Game Ranking
- Stage: RM-3
- Started from next_round: RM-3-R01

## Scope
- Allowed files touched: `packages/discovery/*`, `apps/api/routes/discovery.py`, `tests/test_discovery_search.py`, `.piko/summaries/worker_RM-3-R01.md`
- Files intentionally not touched: real connectors, publishing workflow, deployment, LLM adapters, gates
- Upstream fixes made: none

## Changes
- Modified files:
  - `packages/discovery/rankings.py`
  - `tests/test_discovery_search.py`
- Added files:
  - `.piko/summaries/worker_RM-3-R01.md`
- Deleted files: none
- Behavioral changes: Added `rank_hot_games()` and API fields `real_market_hot_games_top_5` / `real_market_hot_games_top_20` based on normalized `GameHeatSignal` data.

## Task Status
- Execution tasks: completed
- Test tasks: completed
- Collaboration acceptance tasks: Sample Top 5 table included below.

## Verification Run By Worker
- Commands run:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m pytest`
  - API probe `/discovery/rankings?limit=5`
- Results:
  - `59 passed in 2.86s`
  - `139 passed, 3 skipped in 2.96s`
  - `/discovery/rankings?limit=5`: `200`, `mode=fixture`, `real_collection_performed=False`
- Failures: none

## Sample Top 5
| Rank | Game | Ranking Score | Discussion Velocity | Source Diversity |
| --- | --- | ---: | ---: | ---: |
| 1 | Hades II | 83 | 86 | 3 |
| 2 | Stardew Valley | 74 | 74 | 4 |
| 3 | Hollow Knight | 28 | 44 | 3 |

## Sample Output
```json
{
  "mode": "fixture",
  "real_collection_performed": false,
  "real_market_hot_games_top_5_count": 3,
  "top_game": {
    "game_name": "Hades II",
    "ranking_score": 83,
    "discussion_velocity": 86,
    "source_diversity": 3,
    "candidate_only": true
  }
}
```

## Direction Check
- Player need: Hot games are ranked as discovery candidates.
- Source evidence: Ranking uses normalized source metrics only.
- Structured judgment: Output is JSON serializable.
- Clear guide output: Not generated.
- Traceable sources: Region/source signals are retained in each row.
- Risk warnings: Candidate-only; no publishing permission is created.

## Prohibited Items Check
- Default network: no
- Real crawler: no
- Raw text/body/full comments retention: no
- Publishing: no
- Deploy: no
- Default LLM: no
- Gate relaxation: no

## Risks And Notes
- Unfinished: Live real-source ranking remains future opt-in work.
- Risks: Ranking weights are initial heuristics and should be calibrated with real pilot data later.
- Assumptions: Fixture `GameHeatSignal` records stand in for normalized RM-2 connector outputs in default tests.

## Next Recommendation
- Suggested next round: RM-3-R02
- Why: Add hot player question and guide-need ranking buckets.
