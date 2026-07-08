# Piko Growth Loop Queue

Method: Stage-batch file queue workflow.

Purpose:

Build Piko v0.2's daily growth loop. The loop consumes daily GitHub/OSS scan results, converts them into CAP review decisions, generates worker/verify task drafts, and exposes the growth status to the operator. It must remain proposal-only until a human explicitly approves execution.

Stage labels:

- GROW-1 Daily Scan Intake And Normalization
- GROW-2 CAP Review Decisioning
- GROW-3 Worker And Verify Task Draft Generation
- GROW-4 Growth Dashboard And Operator Surface
- GROW-5 Final Verification And Next Loop Readiness

Execution order:

```text
GROW-1-R01 -> GROW-1-R02
GROW-2-R01 -> GROW-2-R02 -> GROW-2-R03
GROW-3-R01 -> GROW-3-R02 -> GROW-3-R03
GROW-4-R01 -> GROW-4-R02
GROW-5-R01 -> GROW-5-R02
```

Relationship to existing queues:

- OSS discovers external projects and architecture patterns.
- CAP governs Piko's capability map.
- GROW connects daily OSS scan results to CAP review and task-draft generation.
- STORY is separate: it creates public-facing GitHub project content and should not be treated as Piko runtime adoption.

Global guardrails:

- Do not auto-run generated worker tasks.
- Do not auto-absorb OSS candidates into active capabilities.
- Do not auto-install plugins, connectors, dependencies, or external repos.
- Do not publish, deploy, commit, push, or use credentials.
- Do not default to network or LLM calls.
- Do not bypass Piko-verify or relax gates.
- Human approval is required before implementation, dependency adoption, credential use, publishing, deployment, destructive replacement, or license-risk adoption.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- Growth artifacts JSON parse probes
- CAP review decision probes
- Worker/verify task draft safety probes
- API/window probes if implemented
- Guardrail scan
