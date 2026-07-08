# Discovery-to-Article Candidate Pipeline Round Queue

Method: Round-by-Round File Queue Workflow.

Status:

```text
Discovery-to-Article queue ready.
Current recommended next round: DA-1-R01
```

Stage labels:

- DA-0 Current Baseline
- DA-1 Candidate Handoff Contract
- DA-2 Candidate Selection From Discovery
- DA-3 Evidence Pipeline Invocation
- DA-4 Draft Artifact Generation
- DA-5 Operator API And CLI
- DA-6 Verification And Safety Gates
- DA-7 Final Documentation And Closeout

Execution order:

```text
DA-0-R01 -> DA-0-R02
DA-1-R01 -> DA-1-R02
DA-2-R01 -> DA-2-R02
DA-3-R01 -> DA-3-R02 -> DA-3-R03
DA-4-R01 -> DA-4-R02
DA-5-R01 -> DA-5-R02
DA-6-R01 -> DA-6-R02
DA-7-R01 -> DA-7-R02
```

Start from DA-1-R01 unless the operator explicitly asks to revisit baseline.

Global guardrails:

- Discovery output is a candidate signal, not publishing permission.
- Default tests must not touch the network.
- Do not publish, deploy, commit, crawl, or store long raw content.
- Generated drafts must remain `publish_ready=false` and `publishing_performed=false`.
- Every candidate draft must pass verification or be clearly blocked.
