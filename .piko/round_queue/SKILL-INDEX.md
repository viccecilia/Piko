# Piko Skill, Content Quality, And Social Distribution Queue

Method: Stage-batch file queue workflow.

Purpose:

This queue absorbs the 2026-07-04 GitHub scan findings into Piko's capability system. It focuses on practical skills that help Piko improve itself and improve what it publishes: skill runtime, worker/verify trace correlation, declarative eval, content quality, and approval-gated social distribution.

Stage labels:

- SKILL-1 Piko Skill Runtime v0
- SKILL-2 Worker Trace And Verify Correlation
- SKILL-3 Declarative Eval Queue
- SKILL-4 Content Quality Engine
- SKILL-5 Social Distribution Skill

Execution order:

```text
SKILL-1-R01 -> SKILL-1-R02
SKILL-2-R01 -> SKILL-2-R02
SKILL-3-R01 -> SKILL-3-R02
SKILL-4-R01 -> SKILL-4-R02 -> SKILL-4-R03
SKILL-5-R01 -> SKILL-5-R02 -> SKILL-5-R03
```

Design principles:

- Absorb patterns, not full external platforms.
- Do not install or vendor third-party projects.
- Improve Piko's output quality before enabling distribution.
- Social publishing must be approval-gated and credential-safe.
- One-click distribution starts as dry-run/package creation unless explicit platform credentials and human approval exist.

Global guardrails:

- Do not publish or upload to any social platform by default.
- Do not store credentials, tokens, cookies, API keys, or authorization headers.
- Do not automate spam, mass posting, or platform policy bypass.
- Do not use scraped copyrighted source text or unlicensed images.
- Do not call LLM by default unless an explicit opt-in path exists.
- Do not bypass verification or relax Gate behavior.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- Skill runtime artifact probes
- Trace/eval artifact probes
- Content quality package probes
- Social distribution dry-run artifact probes
- API/window probes if implemented
- Guardrail scan for publish/upload/secrets/platform bypass
