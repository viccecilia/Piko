# Worker Summary: TD-2-R02

## Round
- Round ID: TD-2-R02
- Round Name: Better Dedup And Representative Questions
- Stage: TD-2 Topic Clustering And Intent Upgrade
- Started from next_round: TD-2-R01

## Scope
- Allowed files touched: `packages/discovery/search_engine.py`, `fixtures/player_questions/*`, `tests/test_discovery_search.py`, `.piko/summaries/worker_TD-2-R02.md`, `.piko/round_status.json`
- Files intentionally not touched: collectors, article generation, publishing paths, deployment config
- Upstream fixes made: none

## Changes
- Modified files: `packages/shared/schemas.py`, `packages/discovery/search_engine.py`, `tests/test_discovery_search.py`, `docs/player_pain_discovery.md`
- Added files: `.piko/summaries/worker_TD-2-R02.md`
- Deleted files: none
- Behavioral changes: representative question selection now uses question heat, evidence quality, language/source readability, and text length; clusters expose `representative_question_id`.

## Before/After Cluster Example
- Before: save-location representative selection was only based on question heat.
- After: `stardew_valley:save_file_location` uses `q_stardew_save_steam_001` as stable representative while preserving the JP example in `representative_questions` and `source_regions`.

## Task Status
- 执行任务: completed
- 测试任务: completed
- 协作验收任务: ready_for_verify

## Verification Run By Worker
- Commands run: `python -m pytest tests\test_discovery_search.py -q`
- Results: `27 passed in 0.53s`
- Failures: none

## Sample Output
```json
{
  "cluster_id": "stardew_valley:save_file_location",
  "representative_question_id": "q_stardew_save_steam_001",
  "representative_questions": [
    "Where is the Stardew Valley save file location on Windows and Steam Deck?",
    "スターデューバレーのセーブデータの場所はどこですか？"
  ],
  "source_regions": [
    "en",
    "jp"
  ],
  "duplicate_count": 13
}
```

## Direction Check
- Player need: repeated save-location questions cluster together.
- Source evidence: source diversity and regions remain visible.
- Structured judgment: representative question id is explicit.
- Clear guide output: no guide is generated.
- Traceable sources: question ids and source regions are preserved.
- Risk warnings: unrelated save-recovery risk remains a separate topic.

## Prohibited Items Check
- Real external API: no
- Real crawler: no
- Real publishing: no
- Admin review / human approval: no
- Minority-language dropping: no
- Over-merge unrelated topics: no

## Risks And Notes
- Unfinished: future semantic dedup can improve beyond deterministic hints.
- Risks: deterministic dedup remains conservative to avoid merging unrelated topics.
- Assumptions: minority-language examples must stay visible even when an English question is the stable representative.

## Next Recommendation
- Suggested next round: TD-2-R03
- Why: multilingual normalization hints should be explicit and documented.
