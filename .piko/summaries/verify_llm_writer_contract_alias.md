# Verify Summary: llm-writer-contract-alias

## Verification Conclusion
- Result: failed
- Round verified: llm-writer-contract-alias
- Summary: code paths and tests for `source_ids` / `used_source_ids` aliasing pass, but an existing live fallback artifact still has `writer_output.source_ids` without `writer_output.used_source_ids`.

## Validation Commands Run
- `python -m pytest`
  - Result: 74 passed, 3 skipped
- `python -m packages.workflows.article_pipeline`
  - Result: status=completed; verification_status=pass; publish_action=draft_review; writer_llm_used=False; `source_ids` equals `used_source_ids`; publishing_performed=False
- `python -m pytest tests\test_content_benchmark.py tests\test_real_source_pilot_2.py -q`
  - Result: 13 passed, 2 skipped
- Direct mock LLM probes:
  - Mock adapter returning `used_source_ids`: WriterAgent emitted matching `source_ids` and `used_source_ids`.
  - Mock adapter returning `source_ids`: WriterAgent emitted matching `source_ids` and `used_source_ids`.
- Artifact scan:
  - `artifacts/article_drafts/stardew-valley-save-file-location.json`: passed alias check.
  - `artifacts/article_drafts/stardew-valley-save-file-location_llm_live.json`: failed alias check.

## Alias Contract Check
- Code path: passed.
- Tests: passed.
- Current default artifact: passed.
- Current live fallback artifact: failed.

Failing artifact details:

```json
{
  "artifact": "artifacts/article_drafts/stardew-valley-save-file-location_llm_live.json",
  "writer_output.source_ids": ["pcgamingwiki_31535"],
  "writer_output.used_source_ids": null,
  "writer_output.llm_used": false,
  "writer_output.llm_fallback_used": true
}
```

## Safety Checks
- `publish_ready=false` in checked artifacts.
- `publishing_performed=false` in checked artifacts.
- Default `PIKO_ENABLE_LLM_WRITER=false` remains unchanged.
- Default `PIKO_LIVE_LLM_TEST=false` remains unchanged.
- Default pipeline did not call LLM.
- No new API route was found.
- No crawler, deploy path, real publishing path, Admin Review backend, or verification relaxation was found.

## Issues Found
- Blocking: `artifacts/article_drafts/stardew-valley-save-file-location_llm_live.json` is stale relative to the new contract. Its fallback `writer_output` has `source_ids` but does not include `used_source_ids`.

## Required Rework
- Regenerate or update `artifacts/article_drafts/stardew-valley-save-file-location_llm_live.json` so `writer_output.used_source_ids` is present and exactly equals `writer_output.source_ids`.
- Add or extend an artifact-level check so all current `artifacts/article_drafts/*.json` writer outputs that contain `source_ids` also contain matching `used_source_ids`.
