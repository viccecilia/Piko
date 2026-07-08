# Verify Summary: llm-writer-contract-alias-artifact-fix

## Verification Conclusion
- Result: passed
- Round verified: llm-writer-contract-alias-artifact-fix
- Summary: the stale live fallback artifact now preserves the real fallback state and contains matching `writer_output.source_ids` and `writer_output.used_source_ids`.

## Validation Commands Run
- `python -m pytest`
  - Result: 75 passed, 3 skipped
- `python -m packages.workflows.article_pipeline`
  - Result: status=completed; verification_status=pass; publish_action=draft_review; writer_llm_used=False; `source_ids` equals `used_source_ids`; publishing_performed=False
- `python -m pytest tests\test_content_benchmark.py tests\test_real_source_pilot_2.py -q`
  - Result: 14 passed, 2 skipped
- Artifact scan over `artifacts/article_drafts/*.json`
  - Result: all writer outputs with source aliases contain both fields and the values match.
- `rg -n "used_source_ids|source_ids|llm_fallback_used|publishing_performed" artifacts/article_drafts tests packages`
  - Result: expected artifact, test, and writer-agent alias references found.
- Prohibited-item scan
  - Result: no new crawler, deploy path, real publishing path, git commit/push, Admin Review backend, or verification relaxation found.

## Artifact Fix Check
- Checked `artifacts/article_drafts/stardew-valley-save-file-location_llm_live.json`.
- The artifact still exists; it was not deleted to avoid the failing check.
- `writer_output.source_ids=["pcgamingwiki_31535"]`.
- `writer_output.used_source_ids=["pcgamingwiki_31535"]`.
- `writer_output.source_ids == writer_output.used_source_ids`.
- `writer_output.llm_used=false`.
- `writer_output.llm_fallback_used=true`.
- `writer_output.llm_error="OpenAI request failed: HTTP 401"`.
- `writer_output.publish_ready=false`.
- `writer_output.publishing_performed=false`.
- Top-level `publish_ready=false` and `publishing_performed=false`.
- The artifact does not pretend the live LLM succeeded.

## Artifact-Level Test Check
- `tests/test_content_benchmark.py` now includes an artifact-level regression test.
- It iterates over `Path("artifacts/article_drafts").glob("*.json")`.
- It checks that any writer output containing either `source_ids` or `used_source_ids` contains both aliases.
- It checks the alias values match.
- It checks top-level artifacts remain unpublished.
- It explicitly checks fallback artifacts remain unpublished and preserve matching aliases.

## Safety Checks
- Default pipeline did not call LLM.
- Default LLM switches were not changed.
- No new API route was added.
- No crawler was added.
- No deploy path was added.
- No real publishing path was added.
- No git repository is present in this working directory, and no commit or push was performed.
- Verification was not relaxed.

## Issues Found
- None.

## Suggested Rework Tasks
- None for this round.
