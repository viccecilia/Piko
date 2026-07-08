# Piko Architecture

Piko is a source-based game guide and player need aggregation platform.

The player-facing brand is **Piko**. Public pages should feel like a useful game companion, not an AI product. Internally, Piko can use agents, retrieval, structured memory, and workflow automation, but public content must read like careful editor work: direct, sourced, risk-aware, and useful.

## Current Scope

Piko currently provides a mock-first, local-safe skeleton through the S8 milestone. It is ready for verification and pre-real-source stabilization, but it is not a production publishing system.

Included:

- FastAPI API skeleton
- `/health`, registry, workflow, verification, eligibility, and feedback endpoints
- Agent Registry V1 and Tool Registry V1
- Placeholder business agents and fact-check agent
- LangGraph-compatible article workflow skeleton
- PostgreSQL model draft
- Local source fixtures
- Evidence card extraction from local fixtures
- Quality gates
- Workflow verification reports
- Publishing eligibility checks that do not deploy
- Disabled-by-default connector interface
- Public guide template with mock content
- Feedback capture as a refresh/verification signal

Excluded:

- Default real Steam, Reddit, Google, ProtonDB, wiki, or search API calls
- Crawlers or scraping
- LLM-based real article generation
- Real publishing or deployment
- Autonomous background agent operation
- Admin review queues or human approval systems

## Core Flow

```text
Player need
-> source selection
-> evidence cards
-> structured memory
-> article brief
-> writer/editor placeholder
-> quality gates
-> verification report
-> publishing eligibility
```

Agents should pass compact structured objects, not full source pages.

## Main Layers

### API

`apps/api` exposes health, registry, gate, workflow, verification, eligibility, and feedback endpoints.

### Agents

`packages/agents` contains placeholder business agents. They currently return deterministic JSON and perform no external calls. Some legacy output field names still include review wording, but no admin review queue or human approval system exists.

### Tools

`packages/shared/tool_registry.py` registers mock tools. Tool definitions explicitly mark whether an external API is required.

### Workflows

`packages/workflows/article_pipeline.py` runs the article workflow from start to end. It uses LangGraph when installed and falls back to a sequential runner if LangGraph is unavailable. The report includes `pipeline_state`, `publish_decision`, `verification_report`, and monitoring metadata.

### Gates

`packages/gates` checks article briefs for intent, evidence, conflicts, risk, original value, readability, fact-check readiness, publishing action, and publishing eligibility.

### Connectors

Real connectors are disabled by default with `PIKO_ENABLE_REAL_CONNECTORS=false`. The MediaWiki/PCGamingWiki connector has an opt-in implementation and mocked tests; local fixtures remain the default development source.

### Database

`packages/db/models.py` defines the first PostgreSQL model draft for games, sources, evidence cards, solution claims, articles, gate results, and structured memory.

## Publishing Boundary

Piko currently never publishes. Even when `publish_decision.value` is `verified_candidate`, `PublishingEligibility.deploy_performed` remains `false`.

`publish_action` is a legacy coarse workflow bucket such as `draft_review`. `publish_decision` is the stricter verification-level decision.
