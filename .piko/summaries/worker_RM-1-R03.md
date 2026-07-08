# Worker Summary: RM-1-R03

## Round
- Round ID: RM-1-R03
- Round Name: Real Source Normalization Schema
- Stage: RM-1
- Started from explicit RM queue request.

## Scope
- Allowed files touched: `packages/discovery/*`, `packages/shared/schemas.py`, `tests/test_discovery_search.py`
- Files intentionally not touched: publishing, deployment, crawler, live collection, LLM defaults, Gates
- Upstream fixes made: none

## Changes
- Modified files:
  - `tests/test_discovery_search.py`
- Added files:
  - `packages/discovery/real_market.py`
  - `.piko/summaries/worker_RM-1-R03.md`
  - `.piko/summaries/worker_RM-1.md`
- Deleted files: none
- Behavioral changes:
  - Added mock-only normalization from source-specific records into `GameHeatSignal` and `PlayerQuestionSignal`.
  - Added per-source summary metadata.
  - Snippets are bounded and raw/body/selftext/content/credentials/authorization fields are dropped from metadata.

## Task Status
- 执行任务: completed
- 测试任务: completed
- 协作验收任务: ready for Piko-verify

## Verification Run By Worker
- Commands run:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m pytest`
- Results:
  - `54 passed in 3.01s`
  - `134 passed, 3 skipped in 3.07s`
- Failures: none

## Sample Output
```json
{
  "hot_game": {
    "game_id": "steam_1",
    "game_name": "Hot Steam Game",
    "region_signals": ["steam", "global"],
    "steam_player_rank": 7,
    "steam_review_velocity": 80,
    "heat_score": 80
  },
  "player_question": {
    "question_id": "steam_q1",
    "game_id": "steam_1",
    "game_name": "Hot Steam Game",
    "question_text": "Where is the save file?",
    "source_type": "steam",
    "snippet": "short snippet",
    "metadata": {
      "source_category": "steam",
      "answer_maturity": "answered",
      "normalized_only": true
    }
  },
  "real_collection_performed": false,
  "candidate_only": true
}
```

## Direction Check
- Player need: mock player-question records normalize into Piko question signals.
- Source evidence: source summaries show counts by source category without raw retention.
- Structured judgment: answer maturity, conflicts, engagement, duplicates, and snippets are normalized fields.
- Clear guide output: no guide or draft generated.
- Traceable sources: source category/title/URL are retained when present.
- Risk warnings: raw text, body, selftext, content, credentials, authorization, and copied table fields are excluded.

## Prohibited Items Check
- Real external API: no
- Real crawler: no
- Real publishing: no
- Admin review / human approval: no
- Unsourced claims: no

## Risks And Notes
- Unfinished: live connectors are intentionally not implemented until RM-2.
- Risks: future source-specific parsers must keep using the sanitization layer and bounded snippets.
- Assumptions: source-specific endpoint payloads can be normalized from mock metadata first.

## Next Recommendation
- Suggested next round: RM-2-R01
- Why: RM-1 contract, opt-in policy, and normalization schema are ready for verification; after verify, RM-2 can implement controlled connectors.
