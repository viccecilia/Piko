# Worker Summary: TD-1-R03

## Round
- Round ID: TD-1-R03
- Round Name: Topic Actionability Classifier
- Stage: TD-1 Topic Scoring Model Upgrade
- Started from next_round: TD-1-R01

## Scope
- Allowed files touched: `packages/shared/schemas.py`, `packages/discovery/scoring.py`, `packages/discovery/search_engine.py`, `fixtures/player_questions/*`, `tests/test_discovery_search.py`, `.piko/summaries/worker_TD-1-R03.md`, `.piko/round_status.json`
- Files intentionally not touched: article generation, source collectors, publishing paths, deployment config
- Upstream fixes made: none

## Changes
- Modified files: `packages/shared/schemas.py`, `packages/discovery/scoring.py`, `packages/discovery/search_engine.py`, `tests/test_discovery_search.py`, `docs/player_pain_discovery.md`
- Added files: `.piko/summaries/worker_TD-1-R03.md`
- Deleted files: none
- Behavioral changes: topic clusters now expose `actionability_label`, `actionability_score`, and `actionability_reasons`.

## Actionability Decisions
- `save_file_location`: `single_page_answerable`
- `crash_after_update` without credible answers: `needs_more_sources`
- `build_loadout`: `too_broad`
- `save_recovery_risk` with high risk: `too_risky`
- `map_exploration_route`: `too_visual`

Topics that should not enter article generation yet:
- `needs_more_sources`
- `too_broad`
- `too_risky`
- `too_visual`

## Task Status
- 执行任务: completed
- 测试任务: completed
- 协作验收任务: ready_for_verify

## Verification Run By Worker
- Commands run: `python -m pytest tests\test_discovery_search.py -q`
- Results: `24 passed in 0.53s`
- Failures: none

## Sample Output
```json
{
  "cluster_id": "stardew_valley:save_file_location",
  "actionability_label": "single_page_answerable",
  "actionability_score": 85,
  "actionability_reasons": [
    "The topic can likely become one focused source-backed Piko page."
  ],
  "publish_ready": false
}
```

## Direction Check
- Player need: actionability is derived from need key, answer status, risk, and evidence quality.
- Source evidence: actionability never fetches or invents sources.
- Structured judgment: labels are explicit and tested.
- Clear guide output: no draft or article is generated.
- Traceable sources: existing source hints remain unchanged.
- Risk warnings: map/image-heavy and risky topics are marked carefully.

## Prohibited Items Check
- Real external API: no
- Real crawler: no
- Real publishing: no
- Admin review / human approval: no
- Copied map/image/table material: no
- Unsourced claims: no article claims generated

## Risks And Notes
- Unfinished: downstream DA/TD stages must respect non-actionable labels before article generation.
- Risks: `too_visual` is conservative and may need source-backed asset policy before real map topics.
- Assumptions: actionability is a prioritization signal, not publishing approval.

## Next Recommendation
- Suggested next round: TD-2-R01 after Piko-verify passes TD-1
- Why: TD-1 scoring model upgrade is complete.
