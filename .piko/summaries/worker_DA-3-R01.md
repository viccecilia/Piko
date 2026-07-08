# Worker Summary: DA-3-R01

## Round
- Round ID: DA-3-R01
- Round Name: Candidate Pipeline Request
- Stage: DA-3
- Started from next_round: DA-3-R01

## Scope
- Allowed files touched: `packages/workflows/*`, `packages/shared/schemas.py`, `tests/test_discovery_search.py`, `.piko/summaries/worker_DA-3-R01.md`
- Files intentionally not touched: publishing, deployment, crawler, real connector defaults, LLM defaults, Gates
- Upstream fixes made: none

## Changes
- Modified files:
  - `packages/shared/schemas.py`
  - `tests/test_discovery_search.py`
- Added files:
  - `packages/workflows/candidate_pipeline.py`
  - `.piko/summaries/worker_DA-3-R01.md`
- Deleted files: none
- Behavioral changes:
  - Added candidate-to-`ArticleWorkflowRequest` mapping.
  - Request now carries optional candidate id, cluster id, article intent, source query hints, and safety metadata while remaining backward-compatible.

## Task Status
- 执行任务: completed
- 测试任务: completed
- 协作验收任务: ready for DA-3 stage verification after R03

## Verification Run By Worker
- Commands run:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m packages.workflows.article_pipeline`
- Results:
  - `42 passed in 2.49s`
  - Article pipeline completed with `workflow=article_pipeline_v1`, `status=completed`, `verification_report.status=pass`.
- Failures: none

## Sample Output
```json
{
  "game_id": "stardew_valley",
  "game_name": "Stardew Valley",
  "player_question": "Where is the Stardew Valley save file location on Windows and Steam Deck?",
  "article_intent": "Help players find and safely back up Stardew Valley save files.",
  "candidate_id": "candidate_stardew_valley_save_file_location",
  "cluster_id": "stardew_valley:save_file_location",
  "publish_ready": false,
  "publishing_performed": false,
  "real_collection_performed": false,
  "safety_metadata": {
    "candidate_only": true,
    "requires_evidence_pipeline": true,
    "decision": "publish_candidate",
    "risk_level": "low"
  }
}
```

## Direction Check
- Player need: candidate request preserves the representative player question.
- Source evidence: request carries source query hints only; it does not collect sources.
- Structured judgment: safety metadata carries decision, risk, candidate type, and required evidence pipeline flags.
- Clear guide output: no guide output generated in this round.
- Traceable sources: source-query hints are preserved for later evidence work.
- Risk warnings: request remains candidate-only and not publish-ready.

## Prohibited Items Check
- Real external API: no
- Real crawler: no
- Real publishing: no
- Admin review / human approval: no
- Unsourced claims: no

## Risks And Notes
- Unfinished: R02/R03 still need runner and verification handoff summaries.
- Risks: candidate workflow may fail verification until source/ranked-step trace alignment improves; wrapper should block publish decisions in that case.
- Assumptions: optional request fields are safe because existing callers do not need to provide them.

## Next Recommendation
- Suggested next round: DA-3-R02
- Why: run the article workflow from a candidate in fixture-safe mode and mirror non-publishing status.
