# Verify Summary: llm-writer-live-pilot

## Verification Conclusion
- Result: passed
- Round verified: llm-writer-live-pilot
- Summary: the LLM writer pilot is default-off, opt-in only, writer-scoped, bounded-input, factchecked, unpublished, and safely falls back to the rule-based writer when live OpenAI access fails.

## Validation Commands Run
- `python -m pytest`
  - Result: 73 passed, 3 skipped
- `python -m packages.workflows.article_pipeline`
  - Result: status=completed; verification_status=pass; publish_action=draft_review; publish_decision=verified_candidate; writer_llm_used=False; real_collection_performed=False; publishing_performed=False
- `python -m pytest tests\test_content_benchmark.py tests\test_real_source_pilot_2.py -q`
  - Result: 12 passed, 2 skipped
- Default config probe
  - Result: `enable_llm_writer=False`; `live_llm_test=False`; `llm_model=gpt-4.1-mini`
- Prompt sanitizer probe
  - Result: `raw_text`, `api_key`, and `secret` fields were excluded; long strings were truncated with `...[truncated]`.
- Prohibited-item and sensitive-data scans with `rg`
  - Result: no persisted API key, bearer token, OpenAI error body, crawler, deploy path, real publishing path, git commit/push, or Admin Review backend found. Hits were expected config names, docs, tests, and the adapter's local Authorization header construction.

## Default LLM Behavior
- Ordinary pytest does not call the LLM.
- `PIKO_ENABLE_LLM_WRITER` defaults to false in `packages/shared/config.py`.
- `PIKO_LIVE_LLM_TEST` defaults to false.
- The live LLM smoke test is skipped unless both `PIKO_ENABLE_LLM_WRITER=true` and `PIKO_LIVE_LLM_TEST=true` are present.
- If `OPENAI_API_KEY` is missing, the live smoke test skips before calling the API.

## LLM Scope Check
- OpenAI access is isolated to `packages/agents/adapters/llm_writer_adapter.py`.
- `WriterAgent` is the only current consumer of `OpenAILLMWriterAdapter`.
- No LLM source discovery, evidence extraction, ranking, factcheck authority, publishing, or deployment path was added.

## LLM Input Boundary Check
- `build_llm_writer_payload(...)` constructs bounded structured payloads from:
  - game
  - player question
  - article intent
  - evidence cards
  - ranked steps
  - risk notes
  - uncertainty notes
- It does not pass full source records, raw full source text, secrets, credentials, API keys, authorization headers, access tokens, refresh tokens, or unbounded webpage content.
- Prompt string values are capped at about 800 characters.

## LLM Output And Verification Check
- Mock accepted LLM output flows through WriterAgent, EditorAgent, FactcheckAgent, and the benchmark verification report.
- Accepted mock LLM output includes/preserves:
  - `claim_trace`
  - source IDs normalized as `source_ids`
  - `risk_notes`
  - `uncertainty_notes`
  - `publish_ready=false`
  - `publishing_performed=false`
- Unsupported mock LLM claim trace is caught:
  - `factcheck_pass=false`
  - `missing_source_ids=["missing_source"]`
  - `missing_evidence_card_ids=["missing_card"]`
  - `verification_report.status=fail`
- Non-blocking note: the raw adapter contract asks the LLM for `used_source_ids`, and the mock LLM returns it, but WriterAgent currently normalizes that field to `source_ids` in persisted `writer_output` instead of preserving a `used_source_ids` alias.

## Live Smoke Artifact Check
- Checked `artifacts/article_drafts/stardew-valley-save-file-location_llm_live.json`.
- Worker attempted live smoke only with explicit opt-in.
- OpenAI returned HTTP 401, so no LLM-authored draft was accepted.
- Artifact remains safe:
  - `llm_used=false`
  - `llm_fallback_used=true`
  - `llm_error="OpenAI request failed: HTTP 401"`
  - `publish_ready=false`
  - `publishing_performed=false`
  - `verification_report.status=pass`
- No API key material or response body was persisted.

## Fallback Check
- With default settings, WriterAgent uses the rule-based source-backed writer.
- When the live LLM adapter fails, WriterAgent falls back to the rule-based draft and records `llm_fallback_used=true`.
- Fallback output keeps `claim_trace`, source IDs, evidence card IDs, `publish_ready=false`, and `publishing_performed=false`.

## Workflow And Publishing Safety
- `python -m packages.workflows.article_pipeline` stayed offline for LLM and completed with:
  - `writer_llm_used=False`
  - `real_collection_performed=False`
  - `verification_status=pass`
  - `publish_action=draft_review`
  - `publishing_performed=False`
- No deploy or publish side effect was found.

## Prohibited Items Check
- No crawler was added.
- No deploy path was added.
- No git repository is present in this working directory, and no commit or push was performed.
- No real publishing was added.
- No Admin Review or human approval backend was added.
- Verification was not bypassed.
- Gates were not relaxed.

## Issues Found
- Non-blocking: persisted successful LLM writer output uses `source_ids` but does not preserve the raw LLM field name `used_source_ids`. The prompt contract still requires `used_source_ids`, and tests use it, but retaining the alias in `writer_output` would make future operator checks clearer.
- Non-blocking: no successful live LLM-authored draft was produced because the available key returned HTTP 401. This is acceptable for this pilot because fallback behavior and safety artifacts were verified.

## Suggested Rework Tasks
- Preserve `used_source_ids` alongside normalized `source_ids` in successful LLM `writer_output`.
- Add an explicit test asserting accepted LLM `writer_output` contains `used_source_ids`, `claim_trace`, `risk_notes`, and `uncertainty_notes`.
