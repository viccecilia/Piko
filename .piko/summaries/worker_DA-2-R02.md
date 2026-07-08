# Worker Summary: DA-2-R02

## Round
- Round ID: DA-2-R02
- Round Name: Candidate Source Query Hints
- Stage: DA-2 Candidate Selection From Discovery
- Started from next_round: DA-2-R01

## Scope
- Allowed files touched: `packages/discovery/*`, `packages/shared/schemas.py`, `tests/test_discovery_search.py`, `.piko/summaries/worker_DA-2-R02.md`, `.piko/round_status.json`
- Files intentionally not touched: collectors, source fetchers, article pipeline runner, publishing paths
- Upstream fixes made: none

## Changes
- Modified files: `packages/discovery/search_engine.py`, `packages/shared/schemas.py`, `tests/test_discovery_search.py`
- Added files: `.piko/summaries/worker_DA-2-R02.md`
- Deleted files: none
- Behavioral changes: article candidates now carry `source_query_hints` and `preferred_source_types` that include game name, player need, source regions, and source types without performing collection.

## Source Hint Example
```json
{
  "candidate_id": "candidate_stardew_valley_save_file_location",
  "source_query_hints": [
    "Stardew Valley save file location",
    "Stardew Valley Where is the Stardew Valley save file location on Windows and Steam Deck?",
    "Stardew Valley save file location en",
    "Stardew Valley save file location jp",
    "Stardew Valley save file location steam_discussion",
    "Stardew Valley save file location wiki_comment"
  ],
  "preferred_source_types": [
    "steam_discussion",
    "wiki_comment"
  ]
}
```

## Task Status
- 执行任务: completed
- 测试任务: completed
- 协作验收任务: ready_for_verify

## Verification Run By Worker
- Commands run: `python -m pytest tests\test_discovery_search.py -q`
- Results: `21 passed in 0.49s`
- Failures: none

## Direction Check
- Player need: hints are generated from the candidate game, need key, and representative question.
- Source evidence: hints prepare later evidence retrieval but do not collect sources.
- Structured judgment: preferred source types are explicit fields.
- Clear guide output: no draft or article is generated.
- Traceable sources: candidate keeps cluster id, source regions, and source type preferences.
- Risk warnings: publish_ready remains false.

## Prohibited Items Check
- Real external API: no
- Real crawler: no
- Real publishing: no
- Admin review / human approval: no
- Unsourced claims: no article claims generated

## Risks And Notes
- Unfinished: DA-3 must still invoke evidence pipeline safely.
- Risks: source query hints are search instructions only, not verified evidence.
- Assumptions: ordinary pytest remains offline.

## Next Recommendation
- Suggested next round: DA-3-R01 after Piko-verify passes DA-2
- Why: candidate selection and source query hints are complete.
