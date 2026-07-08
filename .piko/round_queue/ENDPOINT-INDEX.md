# Piko ENDPOINT Local Approved Endpoint Success Path Queue

Method: Stage-batch file queue workflow.

Purpose:

ENDPOINT creates a local controlled approved JSON endpoint so Piko can prove the live connector success path end-to-end without relying on an external provider. This is a local approved endpoint pilot, not broad real-web coverage.

Stage labels:

- ENDPOINT-1 Local Approved Endpoint Contract
- ENDPOINT-2 Local Endpoint Server And Opt-In
- ENDPOINT-3 Live Connector Success Path
- ENDPOINT-4 REAL Funnel Success Handoff
- ENDPOINT-5 Operator Result And Final Verification

Execution order:

```text
ENDPOINT-1-R01 -> ENDPOINT-1-R02
ENDPOINT-2-R01 -> ENDPOINT-2-R02 -> ENDPOINT-2-R03
ENDPOINT-3-R01 -> ENDPOINT-3-R02
ENDPOINT-4-R01 -> ENDPOINT-4-R02
ENDPOINT-5-R01 -> ENDPOINT-5-R02
```

Boundary:

- This queue may create or expose a local approved JSON endpoint.
- It may set local test opt-in only inside tests/CLI invocation, not as global default.
- It must prove `real_collection_performed=true` only for the bounded local approved endpoint path.
- It must not claim broad internet coverage.

Global guardrails:

- Do not crawl or scrape websites.
- Do not call Steam/Reddit/JP/KR/SERP live connectors.
- Do not save raw response body, full posts, full comments, full pages, images, maps, tables, credentials, tokens, API keys, authorization, or secrets.
- Do not publish, deploy, upload, commit, push, or call LLM by default.
- Do not bypass verification or relax Gate behavior.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- ENDPOINT专项测试
- Local endpoint smoke
- Live connector success path probe
- REAL handoff success artifact probe
- API/window probes if implemented
- Guardrail scan
