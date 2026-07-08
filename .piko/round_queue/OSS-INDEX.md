# Open Source Learning Upgrade Queue

Method: Stage-batch file queue workflow.

Purpose:

Build Piko's controlled open-source learning loop. Every day, Piko can scan or consume GitHub research about high-star projects, identify mature agent frameworks, workflow engines, skills, connectors, evaluation systems, and content automation patterns, then convert them into safe local proposals. OSS does not train models, does not fully self-build an agent runtime, and does not blindly copy third-party code. It learns patterns, creates capability candidates, and hands them to CAP and STORY.

Stage labels:

- OSS-1 Research Intake And Scoring
- OSS-2 Pattern Extraction And Piko Mapping
- OSS-3 Plugin Architecture Upgrade Proposal
- OSS-4 Controlled Implementation Hooks
- OSS-5 Verification, Documentation, And Daily Loop

Execution order:

```text
OSS-1-R01 -> OSS-1-R02 -> OSS-1-R03
OSS-2-R01 -> OSS-2-R02
OSS-3-R01 -> OSS-3-R02 -> OSS-3-R03
OSS-4-R01 -> OSS-4-R02 -> OSS-4-R03
OSS-5-R01 -> OSS-5-R02
```

Relationship to other queues:

- OSS discovers and analyzes external projects.
- CAP decides whether discovered capabilities should be added, replaced, deprecated, or ignored in Piko's capability map.
- STORY turns selected discoveries into WeChat/Xiaohongshu/video draft packages.

Global guardrails:

- Do not auto-apply third-party code.
- Do not vendor external repositories unless explicitly approved in a later dependency/vendor stage.
- Do not copy GPL/AGPL or license-incompatible snippets into Piko source.
- Do not send secrets, credentials, private local files, or proprietary code to external services.
- Do not publish, deploy, commit, push, or auto-apply self-improvement patches.
- Do not bypass Piko verification or relax gates.
- Do not change default network behavior.
- Do not add default LLM calls.
- Output must be proposals, adapters, docs, tests, registries, and safe local abstractions unless a later round explicitly allows implementation.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- Any new OSS/plugin/domain tests added by worker
- JSON parse probes for new artifacts
- Guardrail scan for disallowed vendoring, secrets, crawler behavior, default network, default LLM, publish/deploy side effects, and license misuse
