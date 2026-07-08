# Worker Summary: DA-3-R02

## Round
- Round ID: DA-3-R02
- Round Name: Candidate Workflow Runner
- Stage: DA-3
- Started from next_round: DA-3-R02

## Scope
- Allowed files touched: `packages/workflows/*`, `packages/discovery/*`, `tests/test_discovery_search.py`, `tests/test_content_benchmark.py`, `.piko/summaries/worker_DA-3-R02.md`
- Files intentionally not touched: publishing, deployment, crawler, real connector defaults, LLM defaults, Gates
- Upstream fixes made: candidate wrapper blocks publish decision when workflow verification fails.

## Changes
- Modified files:
  - `tests/test_discovery_search.py`
- Added files:
  - `packages/workflows/candidate_pipeline.py`
  - `.piko/summaries/worker_DA-3-R02.md`
- Deleted files: none
- Behavioral changes:
  - Added `run_candidate_article_workflow(candidate)` for fixture-safe workflow execution from a discovery article candidate.
  - Candidate wrapper mirrors `publish_ready=false`, `publishing_performed=false`, and `real_collection_performed=false`.
  - If the underlying workflow verification fails, candidate-level `publish_decision` is changed to `verification_failed` with `blocks_publish=true`.

## Task Status
- 执行任务: completed
- 测试任务: completed
- 协作验收任务: ready for DA-3 stage verification after R03

## Verification Run By Worker
- Commands run:
  - `python -m pytest tests\test_discovery_search.py tests\test_content_benchmark.py -q`
  - `python -m packages.workflows.article_pipeline`
- Results:
  - `53 passed, 1 skipped in 2.40s`
  - Article pipeline completed with `workflow=article_pipeline_v1`, `status=completed`, `verification_report.status=pass`.
- Failures: none

## Sample Output
```json
{
  "candidate_id": "candidate_stardew_valley_save_file_location",
  "workflow_status": "completed",
  "verification_status": "fail",
  "verification_summary": "fail: 7/8 checks passed.",
  "publish_action": "draft_review",
  "publish_decision": {
    "value": "verification_failed",
    "blocks_publish": true
  },
  "publish_ready": false,
  "publishing_performed": false,
  "real_collection_performed": false,
  "safety_fields": {
    "candidate_only": true,
    "discovery_is_publish_permission": false
  }
}
```

## Direction Check
- Player need: candidate runner preserves Stardew Valley save-location player question.
- Source evidence: workflow uses fixture-safe behavior; no real source collection occurs.
- Structured judgment: verification status and blocking publish decision are mirrored at candidate level.
- Clear guide output: workflow may produce draft-like output internally, but candidate result is not publish-ready.
- Traceable sources: verification checks source/ranked-step trace and can fail when trace is incomplete.
- Risk warnings: failed verification becomes blocking candidate-level decision.

## Prohibited Items Check
- Real external API: no
- Real crawler: no
- Real publishing: no
- Admin review / human approval: no
- Unsourced claims: no publishing claim; failed trace remains blocked.

## Risks And Notes
- Unfinished: R03 still needs final verification handoff checks.
- Risks: Stardew candidate currently fails one verification trace check because default fixture workflow is not yet source-aligned for that game; wrapper blocks publishing accordingly.
- Assumptions: DA-4 can improve artifact generation without changing this candidate-only safety behavior.

## Next Recommendation
- Suggested next round: DA-3-R03
- Why: ensure verification report, publish action, publish decision, and safety fields are consistently returned and non-publishing.
