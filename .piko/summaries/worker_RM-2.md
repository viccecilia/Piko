# Worker Stage Summary: RM-2

## Stage
- Stage ID: RM-2
- Stage Name: Real Market Connectors
- Rounds completed:
  - RM-2-R01
  - RM-2-R02
  - RM-2-R03

## Overall Goal
- Stage goal: Implement controlled real-market connector contracts for Steam, Reddit, SERP/search snippets, JP community, and KR community while keeping default behavior offline.
- Achieved: yes

## Round Results
- Round ID: RM-2-R01
- Status: completed
- Summary file: `.piko/summaries/worker_RM-2-R01.md`
- Verification commands: `python -m pytest tests\test_discovery_search.py -q`
- Result: `57 passed in 2.69s`

- Round ID: RM-2-R02
- Status: completed
- Summary file: `.piko/summaries/worker_RM-2-R02.md`
- Verification commands: `python -m pytest tests\test_discovery_search.py -q`
- Result: `57 passed in 2.69s`

- Round ID: RM-2-R03
- Status: completed
- Summary file: `.piko/summaries/worker_RM-2-R03.md`
- Verification commands: `python -m pytest tests\test_discovery_search.py -q`; `python -m pytest`
- Result: `57 passed in 2.69s`; `137 passed, 3 skipped in 2.92s`

## Files Changed In This Stage
- Modified:
  - `packages/collectors/steam_reviews.py`
  - `packages/collectors/steam_discussions.py`
  - `packages/collectors/reddit.py`
  - `packages/collectors/serp.py`
  - `packages/discovery/real_market.py`
  - `tests/test_discovery_search.py`
  - `.piko/round_status.json`
- Added:
  - `packages/collectors/real_market.py`
  - `packages/collectors/jp_community.py`
  - `packages/collectors/kr_community.py`
  - `.piko/summaries/worker_RM-2-R01.md`
  - `.piko/summaries/worker_RM-2-R02.md`
  - `.piko/summaries/worker_RM-2-R03.md`
  - `.piko/summaries/worker_RM-2.md`
- Deleted: none

## Stage-Level Verification
- Commands run:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m pytest`
  - API probe: `/discovery/search`
  - API probe: `/discovery/real-source/collect`
  - Mock Steam connector normalization probe
- Results:
  - Discovery tests: `57 passed in 2.69s`
  - Full tests: `137 passed, 3 skipped in 2.92s`
  - `/discovery/search`: `200`, `real_collection_performed=False`
  - `/discovery/real-source/collect`: `403`, requires explicit flags
  - Mock connector probe: 1 hot game, 1 question, no `body` retained
- Failures: none

## Stage Direction Check
- Player needs: Connector records represent hot games and player questions as candidate signals.
- Multi-source evidence: Steam, Reddit, SERP, JP, and KR source categories now have safe contracts.
- Structured judgment: All connector outputs normalize through Pydantic `GameHeatSignal` and `PlayerQuestionSignal`.
- Clear guide output: Not generated; discovery remains candidate-only.
- Source traceability: Source titles, URLs, source type, source region, language, and short snippets are preserved when available.
- Risk warnings: Full source bodies, posts, comments, raw page text, credentials, images, maps, and copied tables are not retained.

## Stage Prohibited Items Check
- Default network: no
- Real crawler: no
- Direct Steam/Reddit/JP/KR scraping: no
- Full post/page/comment retention: no
- Publishing: no
- Deploy: no
- Git commit or push: no
- Default LLM: no
- Verification bypass: no
- Gate relaxation: no
- RM-3 executed: no

## Risks
- Remaining risks: Live endpoints are still future work and need sanctioned endpoint review before use.
- Technical debt: Older `RealMarketDiscoverySource` remains as an API-facing adapter; RM-2 adds source-specific collector contracts beside it rather than replacing it.
- What Piko-verify should inspect carefully: Confirm default API collection is still 403, connector tests use injected mock HTTP only, and forbidden fields are not retained in normalized metadata.

## Next Stage
- Next stage: RM-3-R01
- Why: RM-2 connector contracts are complete and should be verified before any scoring/ranking integration work begins.
