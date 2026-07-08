# Self-Improvement Loop

Piko's self-improvement loop is planning-only.

```text
Run -> Verify -> Diagnose -> Propose -> Patch Plan -> Regression Plan -> Ledger -> Operator decision
```

## Allowed Automation

- Collect improvement signals from verification reports.
- Generate diagnostic reports.
- Generate upgrade proposals.
- Generate patch plans.
- Generate regression command plans.
- Generate ledger entries.

## Prohibited Automation

- Applying patches automatically
- Committing changes automatically
- Deploying automatically
- Publishing content automatically
- Opening live connectors automatically
- Bypassing verification
- Changing production behavior from an improvement report

The loop helps a worker or operator decide what to do next. It does not act on its own.

