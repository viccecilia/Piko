# Worker Summary: llm-writer-contract-alias-artifact-fix

## Round
- Round ID: llm-writer-contract-alias-artifact-fix
- Round Name: LLM Writer Contract Alias Artifact Fix Round
- Started from failed verification: llm-writer-contract-alias

## Scope
- Allowed files touched:
  - artifacts/article_drafts/stardew-valley-save-file-location_llm_live.json
  - tests/test_content_benchmark.py
  - .piko/summaries/worker_llm_writer_contract_alias_artifact_fix.md
  - .piko/round_status.json
- Files intentionally not touched:
  - LLM adapter behavior
  - default LLM config switches
  - connector/API/crawler/publishing/deploy behavior
  - verification logic

## Changes
- Fixed stale live fallback artifact:
  - Added `writer_output.used_source_ids`.
  - Kept `writer_output.source_ids`.
  - Ensured both fields are identical.
  - Preserved `llm_used=false`.
  - Preserved `llm_fallback_used=true`.
  - Preserved `publish_ready=false`.
  - Preserved `publishing_performed=false`.
- Added artifact-level regression test:
  - Iterates over `artifacts/article_drafts/*.json`.
  - Requires writer output source alias fields to both exist and match when either alias is present.
  - Requires artifact-level `publish_ready=false`.
  - Requires artifact-level `publishing_performed=false`.
  - Explicitly checks fallback artifacts still satisfy the alias contract and remain unpublished.

## Artifact Scan Sample
```json
{
  "all_ok": true,
  "artifacts": [
    {
      "path": "artifacts\\article_drafts\\stardew-valley-save-file-location.json",
      "source_ids": ["pcgamingwiki_31535"],
      "used_source_ids": ["pcgamingwiki_31535"],
      "alias_equal": true,
      "llm_used": false,
      "llm_fallback_used": false,
      "publish_ready": false,
      "publishing_performed": false
    },
    {
      "path": "artifacts\\article_drafts\\stardew-valley-save-file-location_llm_live.json",
      "source_ids": ["pcgamingwiki_31535"],
      "used_source_ids": ["pcgamingwiki_31535"],
      "alias_equal": true,
      "llm_used": false,
      "llm_fallback_used": true,
      "publish_ready": false,
      "publishing_performed": false
    }
  ]
}
```

## Verification Run By Worker
- Commands run:
  - python -m pytest tests\test_content_benchmark.py tests\test_real_source_pilot_2.py -q
  - python -m packages.workflows.article_pipeline
  - python -m pytest
  - artifact scan over `artifacts/article_drafts/*.json`
- Results:
  - Targeted tests: 14 passed, 2 skipped in 0.25s
  - Article pipeline: status=completed, writer_llm_used=False, source_alias_equal=True, verification_status=pass, publishing_performed=False
  - Full pytest: 75 passed, 3 skipped in 0.72s
  - Artifact scan: all current draft artifacts pass alias and non-publishing checks.
- Failures: none

## Direction Check
- Player need: unchanged.
- Source evidence: unchanged; source ID trace remains `pcgamingwiki_31535`.
- Structured judgment: unchanged.
- Clear guide output: unchanged.
- Traceable sources: improved for stale fallback artifact through `used_source_ids` alias.
- Risk warnings: unchanged.

## Prohibited Items Check
- Real LLM call: not performed.
- Default LLM switch: unchanged.
- New API: not added.
- Real crawler: not added.
- Real publishing: not added.
- Deploy: not performed.
- Verification relaxation: not performed.
- Old artifact deletion: not performed.

## Risks And Notes
- Unfinished: none for this round.
- Risks: Piko-verify should rerun artifact scan against all current `artifacts/article_drafts/*.json` and confirm the live fallback artifact is still a fallback, not a fake successful LLM draft.
- Assumptions: `source_ids` and `used_source_ids` should remain exact aliases for persisted writer outputs.

## Next Recommendation
- Suggested next round: Piko-verify LLM writer contract alias artifact fix verification.
- Why: confirm stale artifact was repaired without changing live LLM, publishing, connector, or verification behavior.
