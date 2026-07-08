# Capability Map And Autonomous System Queue

Method: Stage-batch file queue workflow.

Purpose:

Build a living capability map for Piko. The map tracks local agents, skills, MCP/connectors, external OSS frameworks, replacement candidates, quality scores, risks, and automation boundaries. The long-term goal is a mostly autonomous system where Piko can discover work, choose tools, produce outputs, verify results, propose upgrades, and leave only the final approval to humans.

Stage labels:

- CAP-0 Current Capability Inventory
- CAP-1 Capability Scoring And Replacement Policy
- CAP-2 Skill/Agent/Tool Registry And Routing
- CAP-3 Autonomous Workflow Boundary
- CAP-4 Continuous Capability Optimization Loop

Execution order:

```text
CAP-0-R01 -> CAP-0-R02 -> CAP-0-R03
CAP-1-R01 -> CAP-1-R02 -> CAP-1-R03
CAP-2-R01 -> CAP-2-R02 -> CAP-2-R03
CAP-3-R01 -> CAP-3-R02 -> CAP-3-R03
CAP-4-R01 -> CAP-4-R02
```

Relationship to OSS queue:

- CAP queue should run before OSS-1-to-OSS-5.
- OSS daily GitHub learning should feed candidate capabilities into the CAP map.
- CAP policy decides whether to keep, replace, wrap, downgrade, or reject a capability.

Global guardrails:

- Do not install new plugins/connectors automatically.
- Do not remove or replace existing working agents without verification.
- Do not auto-apply self-improvement patches.
- Do not publish, deploy, commit, push, or bypass verification.
- Human approval remains required for final publishing, external credential use, paid services, license-risk adoption, and destructive replacements.
- Capability map may recommend changes, but runtime changes must go through worker/verify.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- Capability artifact JSON parse probes
- Registry/API/CLI probes if implemented
- Guardrail scan for auto-install, auto-replace, secrets, publishing, deployment, verification bypass
