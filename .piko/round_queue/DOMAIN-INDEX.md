# Piko DOMAIN General Plugin Boundary Queue

Method: Stage-batch file queue workflow.

Purpose:

DOMAIN locks Piko's product boundary: Piko is a domain-agnostic pluggable multi-agent collaboration system. Gaming is only the first domain pack, not the system itself. DOMAIN extracts domain-specific assumptions from core contracts, proves a gaming domain pack can still work, and adds an ai_tools domain pack as a second non-game proof.

Stage labels:

- DOMAIN-1 Core Boundary And Domain Contract
- DOMAIN-2 Gaming Domain Pack Extraction
- DOMAIN-3 AI Tools Domain Pack
- DOMAIN-4 Cross-Domain Workflow Routing
- DOMAIN-5 Domain-Agnostic Operator Surface And Final Verification

Execution order:

```text
DOMAIN-1-R01 -> DOMAIN-1-R02 -> DOMAIN-1-R03
DOMAIN-2-R01 -> DOMAIN-2-R02 -> DOMAIN-2-R03
DOMAIN-3-R01 -> DOMAIN-3-R02 -> DOMAIN-3-R03
DOMAIN-4-R01 -> DOMAIN-4-R02 -> DOMAIN-4-R03
DOMAIN-5-R01 -> DOMAIN-5-R02
```

Product boundary:

- Piko core is domain-agnostic.
- Piko core owns workflow, agent runtime, evidence, scoring interfaces, trace, eval, content quality, distribution dry-run, and verification gates.
- Domain packs own vocabulary, source types, signal normalizers, scoring presets, content templates, risk rules, and operator labels.
- Gaming is one domain pack.
- AI tools is the second proof domain.

Global guardrails:

- Do not remove existing gaming functionality.
- Do not hardcode gaming-only fields in core contracts.
- Do not publish, deploy, commit, push, or call real external APIs.
- Do not default to LLM calls.
- Do not save raw/full source, secrets, credentials, tokens, cookies, API keys, or authorization headers.
- Do not bypass verification or relax Gate behavior.
- Keep all new domain packs candidate/fixture-backed unless explicitly approved.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- DOMAIN专项测试
- Domain artifact JSON parse probes
- Gaming and ai_tools domain fixture probes
- Cross-domain routing probes
- API/window probes if implemented
- Guardrail scan for gaming hardcode in core, publish/deploy, secrets, raw source, verification bypass
