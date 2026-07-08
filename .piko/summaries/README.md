# Piko Worker And Verify Summaries

This folder stores durable handoff summaries between Piko-worker and
Piko-verify.

Naming:

```text
worker_<ROUND_ID>.md
verify_<ROUND_ID>.md
worker_<STAGE_ID>.md
verify_<STAGE_ID>.md
```

Examples:

```text
worker_S1-R01.md
verify_S1-R01.md
worker_S1.md
verify_S1.md
```

Worker summaries are required before `worker_status` can be set to
`ready_for_verify`.

Verify summaries are required before `verification_status` can be set to
`passed`, `failed`, or `conditional`.
