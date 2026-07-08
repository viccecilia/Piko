# RM-1 Stage Verification Summary

Verification result: passed

Verified round: RM-1 Real Market Source Contract
Verified by: Piko-verify
Verified at: 2026-06-23T17:44:50.3084097+09:00

## Validations Run

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
  - Result: passed
- `python -m pytest tests\test_discovery_search.py -q`
  - Result: 54 passed in 2.44s
- `python -m pytest`
  - Result: 134 passed, 3 skipped in 3.72s
- API probe: `POST /discovery/search`
  - Result: 200
  - `real_collection_performed=false`
- API probe: `POST /discovery/real-source/collect`
  - Result: 403 by default
  - Message requires `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true` and `PIKO_LIVE_DISCOVERY_TEST=true`
- Contract and normalization probe
  - Source categories: steam, reddit, jp_community, kr_community, serp_snippet
  - Default collection rejected without opt-in
  - Mock source payloads normalized into 1 `GameHeatSignal` and 5 `PlayerQuestionSignal` records
  - Max retained snippet length: 280 characters
  - Forbidden keys were not retained
- Safety scan
  - `rg -n "crawler|scrape|raw_text|selftext|authorization|api_key|publish_ready.*true|publishing_performed.*true|deploy|git commit|git push" packages apps tests docs`
  - Findings were limited to guardrail docs, tests, schema/model fields, existing opt-in adapters, and forbidden-key definitions. No RM-1 publishing, deployment, crawler, default live collection, or gate-bypass path was found.

## Stage Integrity

Passed.

- `.piko/round_queue/RM-1-R01.md` exists.
- `.piko/round_queue/RM-1-R02.md` exists.
- `.piko/round_queue/RM-1-R03.md` exists.
- `.piko/summaries/worker_RM-1-R01.md` exists.
- `.piko/summaries/worker_RM-1-R02.md` exists.
- `.piko/summaries/worker_RM-1-R03.md` exists.
- `.piko/summaries/worker_RM-1.md` exists.
- Pre-verification status showed:
  - current_round: RM-1
  - worker_status: ready_for_verify
  - verification_status: not_started
  - last_completed_round: RM-1-R03
  - next_round: RM-2-R01

## RM-1-R01 Real Source Contract

Passed.

- Real-market source categories are defined for:
  - Steam
  - Reddit
  - JP community
  - KR community
  - SERP/search snippets
- Hot-game required fields are defined, including game id/name, source category, URL, observed time, rank or velocity, and region.
- Player-question required fields are defined, including question id, game id/name, question text, source metadata, engagement, replies, duplicates, answer maturity, conflict count, and bounded snippet.
- Retained fields and prohibited fields are explicit.
- Prohibited retention includes raw text, full posts/pages, images, maps, credentials, authorization, API keys, copied tables, and raw source bodies.
- Discovery output remains `candidate_only=true`.

## RM-1-R02 Opt-In And Rate-Limit Policy

Passed.

- Real-market collection is disabled by default.
- Collection requires both:
  - `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
  - `PIKO_LIVE_DISCOVERY_TEST=true`
- Endpoint env vars exist for Steam, Reddit, JP community, KR community, and SERP discovery.
- Missing endpoints fail clearly.
- Limits are bounded:
  - max sources: 1 to 5
  - max records per source: 1 to 20
- Timeout and user-agent settings are present.
- Default tests do not require network access.
- Default API probe for `/discovery/real-source/collect` returned 403 rather than collecting.

## RM-1-R03 Real Source Normalization Schema

Passed.

- Source-specific payloads normalize into `GameHeatSignal` and `PlayerQuestionSignal`.
- Source summary metadata is retained without raw body retention.
- Snippets are bounded; probe confirmed maximum retained snippet length of 280 characters.
- Forbidden fields are excluded from normalized output:
  - `raw_text`
  - `body`
  - `selftext`
  - `content`
  - `credentials`
  - `authorization`
  - `table_html`
- Mock coverage includes Steam-like, Reddit-like, JP-like, KR-like, and SERP-like payloads.
- Normalization remains candidate-only and reports `real_collection_performed=false`.

## Guardrail Check

Passed.

- Default path does not touch real sources.
- Real collection requires explicit opt-in.
- No crawler was added.
- No full posts, full pages, images, maps, comments, table bodies, or raw source bodies are retained by RM-1 normalization.
- No publishing was performed.
- No deploy path was added or invoked.
- No default LLM invocation was enabled.
- Discovery output remains a candidate signal, not publishing approval.
- Verification was not bypassed.
- Gates were not relaxed.

## Issues Found

No blocking issues.

Notes:

- Safety scan still finds expected existing strings in docs, tests, schemas, and adapter code, including `raw_text`, `authorization`, and deploy-related policy text. These are guardrail/test references or pre-existing model fields, not RM-1 behavior violations.
- RM-2 must continue to enforce the RM-1 contract before any connector performs live requests.

## Recommended Rework Tasks

None required for RM-1.

Recommended next step:

- Proceed to RM-2-R01 after RM-1 verification status is recorded.
