# REV-2 Stage Verification Summary

Verification result: passed

Verified stage: REV-2 Live Endpoint Opt-In Smoke

Verified by: Piko-verify

Verified at: 2026-06-26T17:45:05.8868269+09:00

## Validations Run

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`: initially failed due UTF-8 BOM, then passed after rewriting `round_status.json` as UTF-8 without BOM.
- `python -m pytest tests\test_discovery_search.py -q`: 67 passed
- `python -m pytest`: 147 passed, 3 skipped
- `python -m packages.discovery.real_endpoint_verify --fixture`: passed
- `python -m packages.discovery.real_endpoint_verify --fixture --write-artifact`: passed and wrote `artifacts/endpoint_verification/latest_endpoint_verification.json`
- `python -m packages.discovery.real_endpoint_verify --live`: skipped safely because live endpoint verification requires explicit opt-in
- Double opt-in without `PIKO_APPROVED_ENDPOINT_URL`: skipped safely with a clear endpoint URL requirement
- Mock-live probe: passed with `mode=mock-live`, 2 games, 4 questions, 2 ranked games, ranking buckets, and `real_collection_performed=false`
- Safety scan for crawler/scrape/raw source/secrets/publish/deploy indicators: reviewed; matches were guardrail definitions, tests, docs, schemas, safe flags, or existing adapters

## Stage Integrity

- `.piko/round_queue/REV-2-R01.md`: present
- `.piko/round_queue/REV-2-R02.md`: present
- `.piko/round_queue/REV-2-R03.md`: present
- `.piko/summaries/worker_REV-2-R01.md`: present
- `.piko/summaries/worker_REV-2-R02.md`: present
- `.piko/summaries/worker_REV-2-R03.md`: present
- `.piko/summaries/worker_REV-2.md`: present
- No `worker_REV-3-R01.md` or `worker_REV-3.md` was found; REV-3 has not been entered.

`round_status.json` matched the expected pre-verification state: `current_round=REV-2`, `worker_status=ready_for_verify`, `verification_status=not_started`, `last_completed_round=REV-2-R03`, `last_verified_round=REV-1`, and `next_round=REV-3-R01`.

## REV-2-R01 Live Endpoint Opt-In Smoke

Passed.

- `packages/discovery/real_endpoint_verify.py` supports controlled live endpoint smoke.
- Live mode requires `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`, `PIKO_LIVE_DISCOVERY_TEST=true`, and either `--url` or `PIKO_APPROVED_ENDPOINT_URL`.
- Default `--live` skipped safely with `real_collection_performed=false`.
- Double opt-in without URL skipped safely and explicitly required `--url` or `PIKO_APPROVED_ENDPOINT_URL`.
- Live fetch path uses configured endpoint only, bounded timeout, bounded payload size, and the approved endpoint contract.
- No raw live response body is written; results expose `raw_response_body_saved=false`.

## REV-2-R02 Live Normalization And Ranking Probe

Passed.

- Fixture endpoint data normalized into 2 hot games and 4 player questions.
- Fixture mode produced 2 ranked games and question ranking buckets.
- Mock-live mode produced ranking preview and buckets while remaining `real_collection_performed=false`.
- Mock-live output uses `mode=mock-live`, so it does not pretend to be real-source collection.
- Skipped live output remains `status=skipped` and does not mark real-source success.

## REV-2-R03 Live Smoke Summary Artifact

Passed.

- `artifacts/endpoint_verification/latest_endpoint_verification.json` exists.
- The artifact contains only bounded summary fields such as status, mode, normalized counts, ranking count, retained fields, skipped reason, safety flags, `real_collection_performed`, `publishing_performed`, and `raw_response_body_saved`.
- The artifact does not contain raw response bodies, full posts, full comments, authorization headers, API keys, secrets, or source payload dumps.
- Literal `body` appears only in the safety flag name `raw_response_body_saved=false`, not as retained source content.

## Guardrail Check

Passed.

- Default tests do not require network access.
- Live endpoint verification remains explicit opt-in.
- No crawler or HTML scraping behavior was introduced.
- No raw/full source body is retained by the endpoint verification flow.
- No publishing or deploy side effects were performed.
- No default LLM or translation API behavior was introduced.
- Discovery output remains candidate/signal-only and does not grant publishing approval.
- Verification and gate behavior were not bypassed or relaxed.

## Findings

No blocking issues found.

Notes:
- `round_status.json` had a UTF-8 BOM before verification; Piko-verify rewrote it as UTF-8 without BOM and the required JSON parse then passed.
- No real approved endpoint URL was configured, so this verification proves default skip, opt-in gating, mock-live behavior, artifact safety, and fixture normalization/ranking, but not a real live endpoint response.

## Recommended Next Work

Proceed to `REV-3-R01`. When a real approved endpoint is configured, rerun the live endpoint verification with explicit opt-in and confirm the same bounded artifact and no-raw-source behavior against the live response.
