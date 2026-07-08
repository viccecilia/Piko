# Piko CONNECTOR General Connector Registry Queue

Method: Stage-batch file queue workflow.

Purpose:

CONNECTOR builds a domain-agnostic connector registry so Piko can attach approved data sources per domain without hardcoding one REAL endpoint or one gaming connector path. It should provide connector manifests, credential policy, source governance, domain routing, dry-run collection plans, and operator visibility. It must not enable broad live crawling or store secrets.

Stage labels:

- CONNECTOR-1 Connector Registry Contract
- CONNECTOR-2 Credential And Permission Boundary
- CONNECTOR-3 Domain Connector Packs
- CONNECTOR-4 Collection Plan And Dry Run
- CONNECTOR-5 Operator Surface And Final Verification

Execution order:

```text
CONNECTOR-1-R01 -> CONNECTOR-1-R02 -> CONNECTOR-1-R03
CONNECTOR-2-R01 -> CONNECTOR-2-R02
CONNECTOR-3-R01 -> CONNECTOR-3-R02 -> CONNECTOR-3-R03
CONNECTOR-4-R01 -> CONNECTOR-4-R02 -> CONNECTOR-4-R03
CONNECTOR-5-R01 -> CONNECTOR-5-R02
```

Product boundary:

- Piko core owns connector registry, connector policy, audit, dry-run planning, and verification gates.
- Domain packs own connector preferences and source priorities.
- Individual connectors own endpoint shape, limits, normalization, and source-specific prohibited fields.
- No connector is active by default unless explicitly approved and verified.

Global guardrails:

- Do not enable default live collection.
- Do not crawl arbitrary websites.
- Do not scrape HTML by default.
- Do not store credentials, tokens, cookies, API keys, authorization headers, refresh tokens, or secrets.
- Do not store raw/full source bodies, full posts, full comments, full pages, images, maps, copied tables, or unbounded snippets.
- Do not publish, deploy, commit, push, or call LLM by default.
- Do not bypass verification or relax Gate behavior.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- CONNECTOR专项测试
- Connector registry artifact JSON parse probes
- Credential guardrail probes
- Domain connector routing probes
- Collection dry-run probes
- API/window probes if implemented
- Guardrail scan
