# Worker Summary: RM-2-R03

## Round
- Round ID: RM-2-R03
- Round Name: JP And KR Community Connectors
- Stage: RM-2
- Started from next_round: RM-2-R01

## Scope
- Allowed files touched: `packages/collectors/*`, `packages/discovery/*`, `tests/test_discovery_search.py`, `.piko/summaries/worker_RM-2-R03.md`, `.piko/summaries/worker_RM-2.md`
- Files intentionally not touched: publishing workflow, deployment, crawler code, LLM adapters, admin review
- Upstream fixes made: Extended prohibited retained metadata with `full_comments` and `raw_page_text`.

## Changes
- Modified files:
  - `packages/discovery/real_market.py`
  - `tests/test_discovery_search.py`
- Added files:
  - `packages/collectors/jp_community.py`
  - `packages/collectors/kr_community.py`
  - `packages/collectors/real_market.py`
- Deleted files: none
- Behavioral changes: JP/KR community connectors preserve source region and language metadata, normalize through the same safe real-market schema, and rely on existing multilingual topic hints without translation or LLM classification.

## Task Status
- Execution tasks: completed
- Test tasks: completed
- Collaboration acceptance tasks: One JP and one KR normalized example are covered below.

## Verification Run By Worker
- Commands run:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m pytest`
  - API probe for `/discovery/search` and `/discovery/real-source/collect`
  - Mock connector normalization probe
- Results:
  - `57 passed in 2.69s`
  - `137 passed, 3 skipped in 2.92s`
  - `/discovery/search`: `200`, `real_collection_performed=False`
  - `/discovery/real-source/collect`: `403` by default
- Failures: none

## Sample Output
```json
{
  "jp": {
    "source_type": "jp_community",
    "source_region": "jp",
    "language": "ja",
    "question_text": "セーブデータの場所はどこですか",
    "normalization_hints": ["save", "location"],
    "full_post_retained": false
  },
  "kr": {
    "source_type": "kr_community",
    "source_region": "kr",
    "language": "ko",
    "question_text": "저장 위치 오류가 있나요",
    "normalization_hints": ["save", "location", "bug"],
    "full_post_retained": false
  }
}
```

## Direction Check
- Player need: JP/KR player questions enter topic discovery as candidate signals.
- Source evidence: Short snippets and source metadata only.
- Structured judgment: Records are normalized to `PlayerQuestionSignal`.
- Clear guide output: Not generated in this round.
- Traceable sources: Source region/language/title/URL fields are preserved when supplied.
- Risk warnings: No translation API, no LLM language classification, no full post retention.

## Prohibited Items Check
- Real external API: not called
- Real crawler: not added
- Real publishing: not performed
- Default network: disabled
- Translation API: not added
- LLM classification: not added
- Full JP/KR post retention: not allowed

## Risks And Notes
- Unfinished: No sanctioned JP/KR endpoints configured.
- Risks: Future connectors need per-source compliance review before live collection.
- Assumptions: Existing multilingual hints are enough for this contract round.

## Next Recommendation
- Suggested next round: RM-3-R01
- Why: RM-2 connector contracts are ready for Piko-verify; RM-3 should only start after verification.
