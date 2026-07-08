# Piko LIVE-CONNECTOR Bounded Live Connector Pilot Queue

Method: Stage-batch file queue workflow.

Purpose:

LIVE-CONNECTOR proves that the CONNECTOR registry can safely move one lowest-risk connector from dry-run planning into a bounded live collection pilot. The first live connector must be `approved_json_endpoint`. It must not crawl, scrape HTML, use broad social platform APIs, or publish.

Stage labels:

- LIVE-CONNECTOR-1 Live Connector Selection And Approval
- LIVE-CONNECTOR-2 Bounded Live Endpoint Probe
- LIVE-CONNECTOR-3 Normalization And Registry Feedback
- LIVE-CONNECTOR-4 REAL Funnel Handoff
- LIVE-CONNECTOR-5 Operator Surface And Final Verification

Execution order:

```text
LIVE-CONNECTOR-1-R01 -> LIVE-CONNECTOR-1-R02
LIVE-CONNECTOR-2-R01 -> LIVE-CONNECTOR-2-R02 -> LIVE-CONNECTOR-2-R03
LIVE-CONNECTOR-3-R01 -> LIVE-CONNECTOR-3-R02
LIVE-CONNECTOR-4-R01 -> LIVE-CONNECTOR-4-R02
LIVE-CONNECTOR-5-R01 -> LIVE-CONNECTOR-5-R02
```

Hard gates:

- Selected connector must be `approved_json_endpoint`.
- Live execution requires:
  - `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
  - `PIKO_LIVE_DISCOVERY_TEST=true`
  - `PIKO_APPROVED_ENDPOINT_URL=<approved JSON endpoint>`
- Missing config must produce `blocked_for_endpoint`.
- Invalid payload shape must produce `failed_contract_validation`.
- No raw response body, full posts, full pages, full comments, credentials, tokens, images, maps, or tables may be stored.
- Live success must be backed by endpoint verification evidence.

Global guardrails:

- Do not enable Steam/Reddit/JP/KR/SERP live connector in this batch.
- Do not crawl or scrape HTML.
- Do not publish, deploy, commit, push, upload, or call LLM by default.
- Do not store secrets, credentials, token, cookie, API key, authorization, or refresh token.
- Do not bypass verification or relax Gate behavior.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- LIVE-CONNECTOR专项测试
- Live connector artifact JSON parse probes
- Endpoint live/blocked probe
- Normalization and REAL handoff probes
- API/window probes if implemented
- Guardrail scan
