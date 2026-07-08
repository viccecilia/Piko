# Verify Summary: real-source-pilot-1

## Scope
- Verification target: Real Source Pilot 1.
- Worker summary checked: `.piko/summaries/worker_real_source_pilot_1.md`.
- Status file checked: `.piko/round_status.json`.
- Live sample checked: `.piko/summaries/real_source_pilot_1_sample.json`.

## Status File Check
- current_round: real-source-pilot-1
- worker_status: ready_for_verify
- verification_status before verify: not_started
- last_verified_round before verify: real-source-pilot-0
- next_round: null

## Required Verification Commands
- `python -m pytest`: passed, 52 passed and 1 skipped.
- `python -m packages.workflows.article_pipeline`: completed.
- `$env:PIKO_ENABLE_REAL_CONNECTORS='true'; $env:PIKO_LIVE_CONNECTOR_TEST='true'; python -m pytest tests/test_stage_5.py -k live_pcgamingwiki_mediawiki_smoke -q`: passed, 1 passed and 6 deselected.

## Live Smoke Check
- A controlled real network request was performed during worker execution and re-run during verification.
- Source family: PCGamingWiki public MediaWiki API only.
- Re-run query: `Hades`.
- Re-run result count: 3 normalized records.
- Double opt-in was required: `PIKO_ENABLE_REAL_CONNECTORS=true` and `PIKO_LIVE_CONNECTOR_TEST=true`.
- After the live command, defaults were confirmed as `enable_real_connectors=False` and `live_connector_test=False`.

## Offline Test Check
- Ordinary `python -m pytest` did not run the live test.
- The live test was skipped by default, proving normal tests do not require live internet.
- Mocked connector tests continue to cover User-Agent, timeout, limit clamp, raw text exclusion, and normalization.

## Normalized Source Record Check
- Saved sample source: `pcgamingwiki_mediawiki_api`.
- Saved sample query: `Hades`.
- Saved sample result count: 3.
- Every record includes `source_id`, `source_type`, `url`, `title`, `retrieved_at`, and `trust_tier`.
- Every record has `source_type=pcgamingwiki`.
- Every record has `raw_text=null`.
- Every record has `metadata.raw_text_included=false`.
- Saved `clean_text` values are short snippets, not long page bodies.

## Workflow Check
- Workflow remains mock-first and does not use real collection by default.
- `status=completed`.
- `verification_report.status=pass`.
- `publish_action=draft_review`.
- `publish_decision.value=verified_candidate`.
- `agent_outputs.source_agent.real_collection_performed=False`.
- `pipeline_state.draft.publishing_performed=False`.

## Prohibited Items Check
- Real external API: yes, but only for the explicitly opted-in PCGamingWiki/MediaWiki live smoke.
- Other live sources: no Reddit, Steam, Google, ProtonDB, or broad web connector was added.
- Crawler/scraper: not added. Code scan found only the MediaWiki API `urlopen` path and no crawler class/function.
- Long raw source storage: not found; sample and connector output keep `raw_text=null`.
- Real publishing/deployment: not introduced.
- Admin Review / human approval backend: not introduced.

## Result
- verification_status: passed
- last_verified_round: real-source-pilot-1
- Verification conclusion: Real Source Pilot 1 is accepted.

## Residual Risks
- Live records are search-result candidates only; they are not yet source-to-evidence extraction.
- PCGamingWiki snippets can contain wiki markup and require a later extraction/cleaning round before player-facing use.
- Real connector use still needs source governance, rate limits, attribution policy, and storage boundaries before expanding beyond controlled smoke tests.
