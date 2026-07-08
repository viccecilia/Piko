# Piko V03 Practical Plugin Absorption Queue

Method: Stage-batch file queue workflow.

Purpose:

V03 moves Piko from a controlled pluggable runtime into a practical first external-capability absorption pilot. The goal is speed to real use, not a broad framework museum. V03 should pick one high-value mature pattern first, implement a bounded adapter around it, run one useful Piko workflow through it, and keep all production activation behind verification and human approval.

Practical target:

- First candidate: LangGraph-style workflow adapter.
- Reason: it maps directly to Piko's workflow orchestration, state, Gate, retry, trace, and multi-agent handoff needs.
- Constraint: do not vendor LangGraph or auto-install dependencies. If LangGraph is unavailable locally, implement the adapter contract and deterministic local fixture so Piko can verify the integration shape now and activate the real package later.

Stage labels:

- V03-1 Practical Plugin Candidate Selection
- V03-2 LangGraph-Style Adapter Pilot
- V03-3 Real Piko Workflow Through Adapter
- V03-4 Operator Approval And Trace Surface
- V03-5 Practical Readiness And Final Verification

Execution order:

```text
V03-1-R01 -> V03-1-R02
V03-2-R01 -> V03-2-R02 -> V03-2-R03
V03-3-R01 -> V03-3-R02
V03-4-R01 -> V03-4-R02
V03-5-R01 -> V03-5-R02
```

Relationship to previous queues:

- GROW finds candidate upgrades.
- CAP scores and governs capabilities.
- V02 created the DomainPlugin and AgentRuntimeAdapter foundation.
- V03 must prove one candidate can become a useful, traceable, approval-gated Piko capability.

Global guardrails:

- Do not install external dependencies by default.
- Do not vendor or copy external repository source.
- Do not replace active runtime automatically.
- Do not call real network, real LLM, or real external APIs by default.
- Do not publish, deploy, commit, push, or use credentials.
- Do not bypass verification or relax Gate behavior.
- Keep all results as candidate/dry-run/internal artifacts until explicit approval.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V03 artifact JSON parse probes
- Adapter fixture tests
- Workflow trace tests
- API/window probes if implemented
- Guardrail scan for install/network/vendor/publish/deploy/verification bypass
