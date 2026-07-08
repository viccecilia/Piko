# Piko V05 Real LangGraph Install Smoke Queue

Method: Stage-batch file queue workflow.

Purpose:

V05 explicitly approves and attempts a real LangGraph installation/probe, records version/import evidence, runs a minimal graph smoke, and then runs the same Piko workflow contract used in V03/V04. V05 is still not production activation.

Stage labels:

- V05-1 Explicit Install Approval
- V05-2 Controlled Dependency Install And Version Probe
- V05-3 Minimal LangGraph Smoke
- V05-4 Piko Workflow On LangGraph Backend
- V05-5 Final Verification And Real Data Handoff Readiness

Execution order:

```text
V05-1-R01 -> V05-1-R02
V05-2-R01 -> V05-2-R02 -> V05-2-R03
V05-3-R01 -> V05-3-R02
V05-4-R01 -> V05-4-R02
V05-5-R01 -> V05-5-R02
```

Hard gates:

- Install is allowed only by V05 explicit approval artifact.
- If install fails, record `blocked_for_dependency` and keep local fixture fallback.
- If import/version probe fails, do not run LangGraph smoke.
- If smoke fails, do not mark backend ready.
- Production activation remains `not_approved_for_production`.

Global guardrails:

- Do not replace active runtime.
- Do not publish, deploy, commit, push, or use credentials.
- Do not call real LLM or real external source connectors.
- Do not vendor LangGraph source.
- Do not bypass verification or relax Gate behavior.
- Keep all outputs as internal pilot artifacts.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V05 artifact JSON parse probes
- LangGraph import/version/install evidence or blocked status tests
- Minimal graph smoke tests
- Piko workflow backend smoke tests
- API/window probes if implemented
- Guardrail scan
