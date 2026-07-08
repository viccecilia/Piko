# Real Endpoint Verification And Live Market Pilot Queue

Method: Continuous multi-stage batch file queue workflow.

Purpose:

Move Piko from safe fixture/mirror discovery into controlled real-market testing through approved JSON endpoints. The target is to prove that Piko can discover current hot games, identify hard player problems, find source-backed solution candidates, generate an internal article package, and show the result in local operator/client surfaces without becoming a crawler and without publishing.

Current prerequisite:

- REV-2 verified passed.
- `round_status.json` should point to `REV-3-R01`.
- Real endpoint live tests require explicit opt-in and approved endpoint URLs. If no endpoint is configured, worker must preserve skipped-live behavior and still complete fixture/mock-live coverage.

Stage labels:

- REV-3 Real Search Endpoint Setup
- REV-4 Real Hot Game And Question Discovery
- REV-5 Real Funnel Candidate Probe
- REV-6 Article Package And Publish-Readiness Surface

Execution order:

```text
REV-3-R01 -> REV-3-R02 -> REV-3-R03
REV-4-R01 -> REV-4-R02 -> REV-4-R03
REV-5-R01 -> REV-5-R02 -> REV-5-R03
REV-6-R01 -> REV-6-R02 -> REV-6-R03
```

Continuous batch rule:

- Execute all REV-3 through REV-6 rounds in order.
- Write one worker summary per round.
- Write one stage worker summary per stage.
- Write one final batch summary: `.piko/summaries/worker_REV-3-to-REV-6.md`.
- Stop only after REV-6-R03.
- Set `worker_status=ready_for_verify`, `verification_status=not_started`, `last_completed_round=REV-6-R03`, `worker_summary_file=.piko/summaries/worker_REV-3-to-REV-6.md`, and `next_round=null`.
- Do not continue into unrelated DA/RM/PD/TD queues.

Global guardrails:

- Default tests must not touch the network.
- Live endpoint verification requires explicit opt-in flags and configured approved endpoint URLs.
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
- Do not bypass verification or relax gates.

Required final verification commands:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --fixture`
- `python -m packages.discovery.real_endpoint_verify --fixture --write-artifact`
- `python -m packages.discovery.real_endpoint_verify --live`
- If approved endpoint env vars are configured, run the explicit opt-in live smoke and report whether it passed or safely skipped.
- Probe `/discovery/funnel-window`, `/discovery/funnel-trace`, `/discovery/rankings`, `/discovery/search`, and the final article/package surface.
