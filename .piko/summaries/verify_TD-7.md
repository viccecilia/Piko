# Verify Summary: TD-7

Stage ID: TD-7
Stage Name: Real Source Pilot For Topic Discovery
Verifier: Piko-verify
Result: passed
Verified at: 2026-06-22T17:58:08.6708887+09:00
Verification mode: idempotent reverify

## Verification Conclusion

TD-7 passed. Worker completed TD-7-R01 and TD-7-R02, generated all required round summaries and the stage summary, and did not enter TD-8.

This was a repeat verification. `round_status.json` was already in `worker_status=complete` and `verification_status=passed` for TD-7 from the previous verification, so Piko-verify treated this as an idempotent recheck and kept `next_round=TD-8-R01`.

TD-7 defines a controlled, default-offline real-source pilot contract for topic discovery. The selected pilot source is PCGamingWiki/MediaWiki metadata, and the smoke path remains fixture-backed unless explicitly opted in. No real collection, crawler, publishing, deployment, or article generation was performed.

## Inputs Reviewed

- `.piko/round_status.json`
- `.piko/round_queue/TD-INDEX.md`
- `.piko/round_queue/TD-7-R01.md`
- `.piko/round_queue/TD-7-R02.md`
- `.piko/summaries/worker_TD-7-R01.md`
- `.piko/summaries/worker_TD-7-R02.md`
- `.piko/summaries/worker_TD-7.md`
- `.piko/summaries/verify_TD-6.md`
- `packages/discovery/real_source.py`
- `packages/discovery/search_engine.py`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`

## Validations Run

- `python -m pytest tests\test_discovery_search.py -q` -> 39 passed
- `python -m pytest` -> 119 passed, 3 skipped
- Live-smoke contract probe -> default skip with clear reason
- Safety scan with `rg` for urlopen/requests/get/post/crawler/scrape/raw_text/publish/deploy indicators in discovery, collectors, tests, and docs

## Stage Integrity

- TD-7 round files present: TD-7-R01, TD-7-R02
- Worker summaries present:
  - `worker_TD-7-R01.md`
  - `worker_TD-7-R02.md`
  - `worker_TD-7.md`
- No `worker_TD-8-R01.md` or `worker_TD-8.md` was found.
- `round_status.json` before this reverify showed:
  - `current_round=TD-7`
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_completed_round=TD-7-R02`
  - `last_verified_round=TD-7`
  - `next_round=TD-8-R01`

## TD-7-R01 Check

Passed. The real-source topic discovery pilot is intentionally narrow and controlled.

Verified contract:

- selected source: `pcgamingwiki_mediawiki`
- source type: `wiki_metadata`
- opt-in flags: `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true` and `PIKO_LIVE_DISCOVERY_TEST=true`
- timeout setting: `PIKO_CONNECTOR_TIMEOUT_SECONDS`, default 5 seconds
- maximum result limit: 3
- retained fields are metadata and short snippets only
- prohibited retention includes raw full page text, full posts, images, maps, copied tables, and credentials

No real network request is performed by the default path.

## TD-7-R02 Check

Passed. Live-smoke contract is default-offline and tested.

Observed contract output:

- `enabled=false`
- `selected_source=pcgamingwiki_mediawiki`
- `max_result_limit=3`
- `real_collection_performed=false`
- skip reason: `Skipped unless PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true and PIKO_LIVE_DISCOVERY_TEST=true.`

Calling `run_discovery_live_smoke("Stardew Valley")` without the two opt-in flags raises the expected skip. Ordinary pytest remains offline and includes live-smoke skip/default-offline coverage.

## Live Smoke / Opt-In Check

- Live smoke requires both opt-in flags.
- Normal pytest does not require network.
- Full pytest result included 3 skipped tests, consistent with live paths remaining opt-in.
- The fixture-backed smoke path caps records and retains only metadata/sample fields.
- No full post/page body is saved.

## Guardrail Check

- No TD-8 execution found.
- No publishing behavior added.
- No deployment behavior added.
- No crawler added.
- No default network collection added.
- No default LLM call added.
- No long raw source storage found.
- No full post/page scraping or retention found in the TD-7 discovery path.
- No verification bypass or gate relaxation found.
- Discovery output remains topic prioritization metadata only, not publishing permission.

## Issues Found

- No blocking issues found.
- Non-blocking: The user repeated a TD-7 verification request after TD-7 had already been verified. Piko-verify handled it as an idempotent reverify and preserved the passed state.
- Non-blocking: Safety scan finds the existing MediaWiki connector's `urlopen` implementation under `packages/collectors/mediawiki.py`; that connector predates TD-7 and remains opt-in/guarded by existing connector controls. TD-7 discovery live-smoke path itself is fixture-backed and default-offline.

## Recommended Follow-Up

- TD-8 may start from `TD-8-R01`.
