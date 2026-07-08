# Piko v0.2 Runtime Growth Queue

Method: Stage-batch file queue workflow.

Purpose:

After GROW proves the daily scan -> CAP review -> draft task loop, V02 turns approved drafts into controlled execution infrastructure. It adds human approval gates, a minimal domain plugin runtime, mature agent framework adapter pilots, eval/observability packs, and a bounded real pilot. V02 must preserve proposal-only behavior until an explicit approval artifact exists.

Stage labels:

- V02-1 Approved Draft To Executable Queue Gate
- V02-2 Minimal Domain Plugin Runtime
- V02-3 Mature Agent Framework Adapter Pilot
- V02-4 Eval Packs And Observability
- V02-5 Controlled Real Pilot And Final Readiness

Execution order:

```text
V02-1-R01 -> V02-1-R02
V02-2-R01 -> V02-2-R02 -> V02-2-R03
V02-3-R01 -> V02-3-R02 -> V02-3-R03
V02-4-R01 -> V02-4-R02 -> V02-4-R03
V02-5-R01 -> V02-5-R02
```

Relationship to previous queues:

- CAP governs which capabilities may be considered.
- GROW produces draft worker/verify tasks from daily scan candidates.
- V02 only materializes or pilots approved drafts and keeps all risky actions behind human approval.

Global guardrails:

- Do not execute draft tasks unless an explicit approval artifact exists.
- Do not auto-install external dependencies, plugins, connectors, or repositories.
- Do not default to network or LLM calls.
- Do not publish, deploy, commit, push, or use credentials.
- Do not replace existing active capabilities without verify approval.
- Do not bypass verification or relax gates.
- Keep all live/real operations behind explicit opt-in and approved endpoint contracts.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V02 artifact JSON parse probes
- Plugin runtime fixture tests
- Adapter contract tests
- Eval/trace artifact tests
- API/window probes if implemented
- Guardrail scan
