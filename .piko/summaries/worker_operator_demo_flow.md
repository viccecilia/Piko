# Worker Summary: operator-demo-flow

## Round
- Round ID: operator-demo-flow
- Round Name: Operator Demo Flow Round
- Started after: llm-writer-contract-alias-artifact-fix verified passed

## Scope
- Allowed files touched:
  - packages/workflows/demo_run.py
  - apps/api/routes/demo.py
  - apps/api/main.py
  - tests/test_operator_demo_flow.py
  - artifacts/demo_runs/*
  - .piko/summaries/worker_operator_demo_flow.md
  - .piko/round_status.json
- Files intentionally not touched:
  - publishing/deploy behavior
  - crawler implementations
  - real connector implementation internals
  - verification gates
  - LLM adapter defaults

## Changes
- Added CLI entry:
  - `python -m packages.workflows.demo_run`
  - Supports `--game-name`, `--question`, `--mode fixture|real-source`, `--use-llm-writer false|true`, and `--output-dir`.
- Added API entry:
  - `POST /demo/run`
  - Request fields: `game_name`, `player_question`, `mode`, `use_llm_writer`.
- Added operator demo helper:
  - Runs the existing multi-agent article pipeline.
  - Writes JSON and Markdown artifacts to `artifacts/demo_runs`.
  - Returns draft, sources, evidence cards, ranked steps, agent trace, verification report, publish action, publish decision, safety fields, and artifact paths.
- Added tests:
  - fixture helper does not call real connector or LLM
  - API returns artifact paths
  - required JSON fields exist
  - default path does not need an API key
  - real-source mode gives a clear error when connectors are disabled
  - LLM request falls back to rule-based writer when LLM is not enabled

## Demo Artifact Sample
```json
{
  "artifact_json": "artifacts\\demo_runs\\20260622T003923Z_example-game-crash-on-startup.json",
  "artifact_md": "artifacts\\demo_runs\\20260622T003923Z_example-game-crash-on-startup.md",
  "verification_status": "pass",
  "publish_ready": false,
  "publishing_performed": false,
  "real_collection_performed": false,
  "llm_used": false,
  "agent_trace_count": 8
}
```

## Verification Run By Worker
- Commands run:
  - python -m pytest tests\test_operator_demo_flow.py -q
  - python -m packages.workflows.demo_run --game-name "Example Game" --question "crash on startup" --mode fixture
  - python -m packages.workflows.article_pipeline
  - python -m pytest
- Results:
  - Demo tests: 4 passed in 0.87s
  - Demo CLI: generated JSON and Markdown artifacts; verification_status=pass; real_collection_performed=False; llm_used=False; publishing_performed=False
  - Article pipeline: status=completed; verification_status=pass; publishing_performed=False; writer_llm_used=False
  - Full pytest: 80 passed, 3 skipped in 0.92s
- Failures: none

## Output Contract
- JSON artifact includes:
  - game_name
  - player_question
  - mode
  - draft
  - sources
  - evidence_cards
  - ranked_steps
  - agent_trace
  - verification_report
  - publish_action
  - publish_decision
  - publish_ready=false
  - publishing_performed=false
  - real_collection_performed
  - llm_used
  - artifact_paths
- Markdown artifact contains the draft body only.

## Direction Check
- Player need: operator enters game_name and player_question.
- Source evidence: demo returns sources and evidence cards from the existing pipeline.
- Structured judgment: demo returns ranked steps and publish decision.
- Clear guide output: demo returns a draft and Markdown artifact.
- Traceable sources: demo returns agent_trace, evidence_cards, and verification_report.
- Risk warnings: demo preserves existing non-publishing and verification behavior.

## Prohibited Items Check
- Real LLM call: not performed by default; disabled fixture tests assert no LLM call.
- Default LLM switch: unchanged.
- Default network/source collection: not performed; fixture tests assert no connector call.
- New API: only local `/demo/run` operator endpoint.
- Real crawler: not added.
- Real publishing: not added; publishing_performed=false.
- Deploy: not performed.
- Verification relaxation: not performed.

## Risks And Notes
- Unfinished: none for this round.
- Risks:
  - `real-source` mode is intentionally blocked unless `PIKO_ENABLE_REAL_CONNECTORS=true`; Piko-verify should confirm the clear error path.
  - The demo writes timestamped artifacts; operators should treat them as internal review artifacts, not public content.
- Assumptions:
  - This is an internal operator flow, not a public frontend or publishing path.

## Next Recommendation
- Suggested next round: Piko-verify Operator Demo Flow verification.
- Why: confirm CLI/API usability, artifact fields, and safety boundaries before any operator-facing documentation or UI layer.
