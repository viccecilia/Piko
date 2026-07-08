# Approved Live Endpoint Queue

Method: Stage-batch file queue workflow.

Purpose:

Connect one approved JSON endpoint for a small real-market live smoke. The goal is to prove Piko can touch real market data safely: fetch bounded hot game/player-question signals, normalize them, generate a live verification artifact, and show the result in operator surfaces without crawling, raw source retention, publishing, deployment, default LLM, translation API, or image generation.

Current prerequisite:

- REV-3-to-REV-6 verified passed.
- `round_status.json` should point to `LIVE-1-R01`.
- Operator must provide an approved JSON endpoint URL before a real live pass can happen. If no URL is configured, worker must preserve safe skipped-live behavior and clearly report what is missing.

Stage labels:

- LIVE-1 Approved Live Endpoint Connection

Execution order:

```text
LIVE-1-R01 -> LIVE-1-R02 -> LIVE-1-R03
```

Stage-batch rule:

- Execute all LIVE-1 rounds in order.
- Write one worker summary per round.
- Write one stage worker summary: `.piko/summaries/worker_LIVE-1.md`.
- Stop after LIVE-1-R03.
- Set `worker_status=ready_for_verify`, `verification_status=not_started`, `last_completed_round=LIVE-1-R03`, `worker_summary_file=.piko/summaries/worker_LIVE-1.md`, and `next_round=null`.

Required endpoint contract:

- Endpoint must return JSON, not HTML.
- Root payload must follow the approved endpoint contract already implemented in REV:
  - `source`
  - `generated_at`
  - `metadata`
  - `games`
  - `questions`
- Games/questions must normalize into `GameHeatSignal` and `PlayerQuestionSignal`.
- Snippets must be short and bounded.
- Raw/full text fields must be rejected or discarded.

Expected environment variables:

- `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
- `PIKO_LIVE_DISCOVERY_TEST=true`
- `PIKO_APPROVED_ENDPOINT_URL=<approved-json-endpoint>`

Global guardrails:

- Default tests must not touch the network.
- Live endpoint verification requires explicit opt-in flags and configured approved endpoint URL.
- Only approved JSON endpoints are allowed.
- Do not crawl websites.
- Do not scrape HTML pages.
- Do not store full posts, full pages, full comments, raw response bodies, images, maps, copied tables, credentials, API keys, authorization headers, or secrets.
- Keep snippets short and bounded.
- Discovery output is candidate signal only, not publishing permission.
- Article output remains internal draft/review unless a later explicit publish stage is created and verified.
- Do not publish, deploy, commit, push, or auto-apply self-improvement patches.
- Do not default-call LLMs.
- Do not call translation APIs.
- Do not generate or download images.
- Do not bypass verification or relax gates.

Required verification commands:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --fixture`
- `python -m packages.discovery.real_endpoint_verify --fixture --write-artifact`
- `python -m packages.discovery.real_endpoint_verify --live`
- If endpoint env vars are configured, run explicit opt-in live verification and record whether `real_collection_performed=true`.
