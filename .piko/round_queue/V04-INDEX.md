# Piko V04 Real LangGraph Backend Approval Pilot Queue

Method: Stage-batch file queue workflow.

Purpose:

V04 turns the V03 LangGraph-style local adapter pilot into a controlled real-backend approval pilot. The worker may execute V04-1 through V04-5 in one continuous batch, and Piko-verify should verify the whole batch once at the end.

Important:

This is not production activation. V04 may prove that a real LangGraph backend can be approved, installed/probed, and run through the same Piko workflow contract. It must not replace the active runtime, publish, deploy, or bypass verification.

Stage labels:

- V04-1 Approval And Dependency Review
- V04-2 Controlled LangGraph Backend Install Probe
- V04-3 Backend Adapter Implementation
- V04-4 Real Backend Smoke Workflow
- V04-5 Final Verification And Activation Readiness

Execution order:

```text
V04-1-R01 -> V04-1-R02
V04-2-R01 -> V04-2-R02 -> V04-2-R03
V04-3-R01 -> V04-3-R02
V04-4-R01 -> V04-4-R02
V04-5-R01 -> V04-5-R02
```

Hard gates:

- If no explicit approval artifact exists, dependency install/probe must stop as `blocked_for_approval`.
- If approval exists but dependency install/probe fails, stop as `blocked_for_dependency` or `needs_fix`.
- If LangGraph is unavailable, keep local fixture working and do not pretend real backend success.
- Production activation must remain `not_approved_for_production`.

Global guardrails:

- Do not replace active runtime.
- Do not publish, deploy, commit, push, or use credentials.
- Do not call real external workflow APIs, real LLM, or real connectors by default.
- Do not vendor LangGraph source or copy external repository code.
- Do not bypass verification or relax Gate behavior.
- Keep all outputs as internal pilot / approval-required artifacts.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V04 artifact JSON parse probes
- LangGraph backend availability/probe test or explicit blocked status test
- Backend selector tests
- Workflow smoke tests
- API/window probes if implemented
- Guardrail scan for active replacement, publish/deploy, vendor source, secrets, verification bypass
