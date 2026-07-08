# Piko EXTERNAL-ENDPOINT Approved External Endpoint Pilot Queue

Method: Stage-batch file queue workflow.

Purpose:

EXTERNAL-ENDPOINT moves Piko from local approved endpoint success to a real external approved JSON endpoint pilot. It verifies an operator-approved external JSON endpoint under bounded constraints, normalizes returned signals, hands them to the REAL funnel, and produces internal candidate artifacts. It must not crawl, scrape, publish, or claim broad internet coverage beyond the approved endpoint.

Stage labels:

- EXTERNAL-ENDPOINT-1 External Endpoint Approval And Contract
- EXTERNAL-ENDPOINT-2 Bounded External HTTP Probe
- EXTERNAL-ENDPOINT-3 External Signal Normalization
- EXTERNAL-ENDPOINT-4 REAL Funnel And Candidate Package
- EXTERNAL-ENDPOINT-5 Operator Surface And Final Verification

Execution order:

```text
EXTERNAL-ENDPOINT-1-R01 -> EXTERNAL-ENDPOINT-1-R02
EXTERNAL-ENDPOINT-2-R01 -> EXTERNAL-ENDPOINT-2-R02 -> EXTERNAL-ENDPOINT-2-R03
EXTERNAL-ENDPOINT-3-R01 -> EXTERNAL-ENDPOINT-3-R02
EXTERNAL-ENDPOINT-4-R01 -> EXTERNAL-ENDPOINT-4-R02
EXTERNAL-ENDPOINT-5-R01 -> EXTERNAL-ENDPOINT-5-R02
```

Hard gates:

- External endpoint requires explicit operator-approved URL.
- Required opt-in:
  - `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
  - `PIKO_LIVE_DISCOVERY_TEST=true`
  - `PIKO_APPROVED_ENDPOINT_URL=<external approved JSON endpoint>`
- Missing URL or opt-in must produce `blocked_for_external_endpoint`.
- Invalid JSON contract must produce `failed_contract_validation`.
- Success scope must be `external_approved_endpoint`, not broad internet coverage.

Global guardrails:

- Do not crawl or scrape websites.
- Do not enable Steam/Reddit/JP/KR/SERP broad live connectors.
- Do not save raw response body, full posts, full pages, full comments, images, maps, tables, credentials, token, cookie, API key, authorization, or secrets.
- Do not publish, upload, deploy, commit, push, or call LLM by default.
- Do not bypass verification or relax Gate behavior.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- EXTERNAL-ENDPOINT专项测试
- External endpoint blocked/success probe
- Contract validation probe
- REAL handoff and article candidate probes
- API/window probes if implemented
- Guardrail scan
