# Topic Discovery Strengthening Round Queue

Method: Stage-by-Stage Batch Execution.

Status:

```text
Topic Discovery Strengthening batch completed.
Current authority: .piko/round_status.json
Initial implementation round: TD-1-R01
Next recommended work: DA-3-R01
```

Stage labels:

- TD-0 Current Discovery Baseline
- TD-1 Topic Scoring Model Upgrade
- TD-2 Topic Clustering And Intent Upgrade
- TD-3 Source Coverage And Region Signals
- TD-4 Competition Gap And Content Opportunity
- TD-5 Watchlist Monitoring Logic
- TD-6 Topic Search API And CLI
- TD-7 Real Source Pilot For Topic Discovery
- TD-8 Final Verification And Resume DA

Execution order:

```text
TD-0-R01 -> TD-0-R02
TD-1-R01 -> TD-1-R02 -> TD-1-R03
TD-2-R01 -> TD-2-R02 -> TD-2-R03
TD-3-R01 -> TD-3-R02
TD-4-R01 -> TD-4-R02 -> TD-4-R03
TD-5-R01 -> TD-5-R02
TD-6-R01 -> TD-6-R02
TD-7-R01 -> TD-7-R02
TD-8-R01 -> TD-8-R02
```

Start from the `next_round` value in `.piko/round_status.json`.
The queue contains 21 executable TD round files plus this index file.
TD-0 is baseline inventory; normal implementation starts from TD-1-R01 unless the operator explicitly asks to revisit baseline.

Global guardrails:

- Topic discovery output is a prioritization signal, not publishing permission.
- Default tests must not touch the network.
- Real community collection requires explicit opt-in.
- Do not publish, deploy, commit, crawl, or store long raw content.
- Do not copy full posts, articles, images, maps, or tables.
- Watchlist topics must not be converted to article drafts until answer/evidence maturity improves.
