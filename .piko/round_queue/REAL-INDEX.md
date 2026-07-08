# Piko REAL Real Data Market Pilot Queue

Method: Stage-batch file queue workflow.

Purpose:

REAL moves Piko from runtime readiness into real approved data usage. It should use an approved JSON endpoint or approved real source configuration to collect bounded live market signals, rank hot games and player pain points, select a safe content candidate, and generate an internal source-backed article package. It must not publish automatically.

Stage labels:

- REAL-1 Approved Live Data Readiness
- REAL-2 Real Market Collection And Normalization
- REAL-3 Live Funnel Ranking And Topic Selection
- REAL-4 Source-Backed Candidate Article Package
- REAL-5 Operator Result And Final Verification

Execution order:

```text
REAL-1-R01 -> REAL-1-R02
REAL-2-R01 -> REAL-2-R02 -> REAL-2-R03
REAL-3-R01 -> REAL-3-R02 -> REAL-3-R03
REAL-4-R01 -> REAL-4-R02
REAL-5-R01 -> REAL-5-R02
```

Hard gates:

- Real collection requires explicit opt-in:
  - `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
  - `PIKO_LIVE_DISCOVERY_TEST=true`
  - approved endpoint URL via CLI or `PIKO_APPROVED_ENDPOINT_URL`
- If endpoint is missing, stop as `blocked_for_endpoint`.
- If endpoint returns invalid shape, stop as `failed_contract_validation`.
- If real collection succeeds, `real_collection_performed=true` must be supported by artifact evidence.
- No crawler, no raw/full source storage, no HTML scrape.
- No publish/deploy. Article output remains internal candidate only.

Global guardrails:

- Do not crawl arbitrary websites.
- Do not save raw response body, full posts, full comments, full pages, images, maps, tables, credentials, authorization, API keys, or secrets.
- Do not call LLM by default.
- Do not publish, deploy, commit, push, or auto-post.
- Do not bypass verification or relax Gate behavior.
- Keep all outputs as candidate/internal artifacts until human approval.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- Real endpoint live/blocked verification
- Real collection artifact JSON parse probes
- Funnel/ranking artifact probes
- Article package safety probes
- API/window probes if implemented
- Guardrail scan
