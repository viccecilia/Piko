# Real Market Discovery Round Queue

Method: Stage-batch file queue workflow.

Purpose:

Build controlled real-market discovery so Piko can find current hot games, hot player questions, answer maturity, and guide opportunities across Steam, Reddit, JP/KR communities, and search snippets without becoming an uncontrolled crawler.

Current prerequisite:

- DA-4 should be verified before production-style RM work continues.
- If the operator explicitly pauses DA and starts RM, worker may execute RM from RM-1-R01.

Stage labels:

- RM-1 Real Market Source Contract
- RM-2 Real Market Connectors
- RM-3 Real Market Ranking And Client Surface
- RM-4 Real Market Pilot And Verification

Execution order:

```text
RM-1-R01 -> RM-1-R02 -> RM-1-R03
RM-2-R01 -> RM-2-R02 -> RM-2-R03
RM-3-R01 -> RM-3-R02 -> RM-3-R03
RM-4-R01 -> RM-4-R02 -> RM-4-R03
```

Stage-batch rule:

- Execute every round in the current stage.
- Write one worker summary per round.
- Write one stage worker summary.
- Stop at the end of the stage and set `worker_status=ready_for_verify`.
- Do not enter the next stage until Piko-verify passes the current stage.

Global guardrails:

- Default tests must not touch the network.
- Real collection requires explicit opt-in flags.
- Do not crawl whole sites.
- Do not scrape or store full posts, full pages, images, maps, comments, tables, or raw source bodies.
- Keep retained text snippets short and bounded.
- Discovery output is candidate signal only, not publishing permission.
- Do not publish, deploy, commit, push, or auto-apply self-improvement patches.
- Do not bypass verification or relax existing gates.
- Do not enable default LLM calls.
