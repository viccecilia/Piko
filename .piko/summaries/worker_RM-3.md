# Worker Stage Summary: RM-3

## Stage
- Stage ID: RM-3
- Stage Name: Real Market Ranking And Client Surface
- Rounds completed:
  - RM-3-R01
  - RM-3-R02
  - RM-3-R03

## Overall Goal
- Stage goal: Connect RM-2 normalized connector outputs to ranking and client surfaces while keeping default behavior offline.
- Achieved: yes

## Round Results
- Round ID: RM-3-R01
- Status: completed
- Summary file: `.piko/summaries/worker_RM-3-R01.md`
- Verification commands: `python -m pytest tests\test_discovery_search.py -q`
- Result: `59 passed in 2.86s`

- Round ID: RM-3-R02
- Status: completed
- Summary file: `.piko/summaries/worker_RM-3-R02.md`
- Verification commands: `python -m pytest tests\test_discovery_search.py -q`
- Result: `59 passed in 2.86s`

- Round ID: RM-3-R03
- Status: completed
- Summary file: `.piko/summaries/worker_RM-3-R03.md`
- Verification commands: `python -m pytest tests\test_discovery_search.py -q`; `python -m pytest`
- Result: `59 passed in 2.86s`; `139 passed, 3 skipped in 2.96s`

## Files Changed In This Stage
- Modified:
  - `packages/discovery/rankings.py`
  - `apps/api/routes/discovery.py`
  - `tests/test_discovery_search.py`
  - `.piko/round_status.json`
- Added:
  - `.piko/summaries/worker_RM-3-R01.md`
  - `.piko/summaries/worker_RM-3-R02.md`
  - `.piko/summaries/worker_RM-3-R03.md`
  - `.piko/summaries/worker_RM-3.md`
- Deleted: none

## Stage-Level Verification
- Commands run:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m pytest`
  - API probe `/discovery/rankings?limit=5`
  - API probe `/discovery/search`
  - API probe `/discovery/real-source/collect`
  - Window smoke `/discovery/window`
- Results:
  - Discovery tests: `59 passed in 2.86s`
  - Full tests: `139 passed, 3 skipped in 2.96s`
  - Rankings probe: `200`, `mode=fixture`, `real_collection_performed=False`, 3 hot-game rows, 5 bucket keys
  - Search probe: `200`, `real_collection_performed=False`
  - Real-source collect probe: `403` by default
  - Window smoke: required ranking section labels present
- Failures: none

## Stage Direction Check
- Player needs: Hot games and hot questions are ranked for operator discovery.
- Multi-source evidence: Ranking accepts normalized source metrics and preserves mode.
- Structured judgment: Outputs are JSON serializable sections and buckets.
- Clear guide output: Not generated; discovery remains candidate-only.
- Source traceability: Ranking rows keep region/source signals and cluster-derived source context.
- Risk warnings: Watchlist rows are non-runnable, high-risk rows are not publish candidates, and publishing remains false.

## Stage Prohibited Items Check
- Default network: no
- Crawler: no
- Full source scrape or retention: no
- `raw_text` / `body` / `selftext` / `content` / `full_comments` / `raw_page_text` retention: no
- Publishing: no
- Deploy: no
- Default LLM: no
- Translation API: no
- Verification bypass: no
- Gate relaxation: no
- RM-4 executed: no

## Risks
- Remaining risks: Ranking weights are initial and need calibration after controlled live market pilots.
- Technical debt: Existing discovery window still has legacy mojibake copy; RM-3 added stable ASCII labels for new sections instead of rewriting the full UI.
- What Piko-verify should inspect carefully: Confirm `/discovery/rankings` has the new hot-game and bucket fields, `/discovery/window` does not trigger real source collection by default, and high-risk/watchlist topics remain blocked/non-runnable.

## Next Stage
- Next stage: RM-4-R01
- Why: RM-3 ranking/client surface is ready for verification; RM-4 should only proceed after Piko-verify passes this stage.
