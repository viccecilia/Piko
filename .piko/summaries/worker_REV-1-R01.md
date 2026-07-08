# Worker Summary: REV-1-R01

## Round
- Round ID: REV-1-R01
- Round Name: Approved Endpoint Contract
- Stage: REV-1
- Started from next_round: null, operator explicitly started REV-1-R01

## Scope
- Allowed files touched: `docs/*`, `packages/discovery/*`, `tests/test_discovery_search.py`, `.piko/summaries/worker_REV-1-R01.md`
- Files intentionally not touched: live connector defaults, publishing, deployment, gates, LLM adapters
- Upstream fixes made: none

## Changes
- Modified files:
  - `docs/player_pain_discovery.md`
  - `tests/test_discovery_search.py`
- Added files:
  - `packages/discovery/real_endpoint_contract.py`
  - `.piko/summaries/worker_REV-1-R01.md`
- Deleted files: none
- Behavioral changes: Added approved JSON endpoint contract validation and rejection of HTML/raw/full-source payload shapes.

## Task Status
- Execution tasks: completed
- Test tasks: completed
- Collaboration acceptance tasks: Valid and rejected examples included below.

## Verification Run By Worker
- Commands run:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m pytest`
- Results:
  - `65 passed in 2.76s`
  - `145 passed, 3 skipped in 4.26s`
- Failures: none

## Valid Endpoint JSON Example
```json
{
  "source": {
    "source_id": "fixture_mirror_market_001",
    "source_type": "approved_market_json",
    "source_category": "steam",
    "endpoint_type": "json"
  },
  "generated_at": "2026-06-24T00:00:00Z",
  "metadata": {"candidate_only": true},
  "games": [{"game_id": "hades_ii", "game_name": "Hades II", "source_category": "steam"}],
  "questions": [{"question_id": "rev_q_answered_001", "question_text": "Where is the save file?", "snippet": "Short snippet only."}]
}
```

## Rejected Example
```json
{
  "source": {"endpoint_type": "html"},
  "questions": [{"raw_text": "full copied source must not pass"}]
}
```

## Direction Check
- Player need: Endpoint contract supports hot games and player questions.
- Source evidence: Only approved JSON metadata and bounded snippets are allowed.
- Structured judgment: Contract validates root/source/game/question fields.
- Clear guide output: Not generated.
- Traceable sources: `source` metadata and URL fields are required or retained.
- Risk warnings: HTML, raw body endpoints, and prohibited fields are rejected.

## Prohibited Items Check
- Live endpoint call: no
- HTML scraping: no
- Publishing/deployment: no
- Raw/full source retention: no

## Risks And Notes
- Unfinished: No real endpoint was verified in this round.
- Risks: Future live endpoints must conform to this JSON contract before use.
- Assumptions: `source_category` maps to the existing real-market normalizer categories.

## Next Recommendation
- Suggested next round: REV-1-R02
- Why: Add local fixture mirror payload that follows the contract.
