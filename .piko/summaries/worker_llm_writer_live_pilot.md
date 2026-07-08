# Worker Summary: llm-writer-live-pilot

## Round
- Round ID: llm-writer-live-pilot
- Round Name: LLM Writer Live Pilot
- Started after: artifact-safety-mirror verified passed

## Scope
- Allowed files touched:
  - packages/agents/adapters/llm_writer_adapter.py
  - packages/agents/writer_agent.py
  - packages/agents/factcheck_agent.py
  - packages/shared/config.py
  - packages/workflows/article_pipeline.py
  - packages/workflows/content_benchmark.py
  - tests/test_content_benchmark.py
  - docs/current_state.md
  - docs/source_policy.md
  - artifacts/article_drafts/*
  - artifacts/comparisons/*
  - .piko/summaries/*
  - .piko/round_status.json
- Files intentionally not touched:
  - connector implementations beyond existing behavior
  - publishing/deploy behavior
  - crawler or scraping code
  - admin review or human approval systems

## Changes
- Added optional LLM writer adapter:
  - packages/agents/adapters/llm_writer_adapter.py
- Added config switches:
  - PIKO_ENABLE_LLM_WRITER=false by default
  - PIKO_LIVE_LLM_TEST=false by default
  - PIKO_LLM_MODEL defaults to gpt-4.1-mini
  - PIKO_LLM_TIMEOUT_SECONDS defaults to 20 seconds
- Updated WriterAgent:
  - Uses LLM only when PIKO_ENABLE_LLM_WRITER=true.
  - Sends only bounded structured inputs: game, player question, article intent, evidence cards, ranked steps, source IDs, short snippets already on evidence cards, risk notes, and uncertainty notes.
  - Does not pass raw_text, credentials, secrets, tokens, API keys, or full webpage bodies.
  - Falls back to rule-based writer on missing key, HTTP failure, or malformed LLM output.
  - Always returns publish_ready=false and publishing_performed=false.
- Updated article_pipeline:
  - Passes existing sources, evidence cards, ranked steps, risk notes, and uncertainty notes to WriterAgent when available.
- Updated content_benchmark:
  - Mirrors llm_used, llm_fallback_used, and llm_error at the artifact top level.
  - Adds a benchmark verification_report mirror for source trace, evidence trace, factcheck, and publishing side-effect checks.
- Updated FactcheckAgent:
  - Checks writer claim_trace source_id and evidence_card_id against actual evidence cards.
  - Fails factcheck when writer/LLM claim trace points to missing sources or missing evidence cards.
- Updated docs:
  - docs/current_state.md
  - docs/source_policy.md
- Added tests:
  - default rule-based writer path requires no API key
  - mock LLM writer output flows through artifact, FactcheckAgent, and verification_report
  - unsupported LLM claim trace is caught by factcheck/verification
  - live LLM smoke remains skipped unless explicitly opted in

## Live LLM Smoke
- Real request attempted: yes
- Explicit opt-in used:
  - PIKO_ENABLE_LLM_WRITER=true
  - PIKO_LIVE_LLM_TEST=true
- Source/query: existing Stardew Valley source sample from real-source pilot content benchmark
- Model configured: gpt-4.1-mini
- Input evidence count: 4
- Result: OpenAI returned HTTP 401, so no LLM-authored draft was accepted.
- Fallback: yes, rule-based WriterAgent output was used.
- Output artifact paths:
  - artifacts/article_drafts/stardew-valley-save-file-location_llm_live.json
  - artifacts/article_drafts/stardew-valley-save-file-location_llm_live.md
- verification_report.status: pass
- publish_ready: false
- publishing_performed: false
- Sensitive data note: adapter error handling was tightened after the failed live request; saved artifacts now only record "OpenAI request failed: HTTP 401" and do not store response bodies or API key material.

## Default Artifact Sample
```json
{
  "llm_used": false,
  "publish_ready": false,
  "publishing_performed": false,
  "verification_report_status": "pass"
}
```

## Live Smoke Artifact Sample
```json
{
  "llm_used": false,
  "llm_fallback_used": true,
  "llm_error": "OpenAI request failed: HTTP 401",
  "publish_ready": false,
  "publishing_performed": false,
  "verification_report_status": "pass"
}
```

## Verification Run By Worker
- Commands run:
  - python -m pytest tests\test_content_benchmark.py tests\test_real_source_pilot_2.py -q
  - python -m packages.workflows.article_pipeline
  - python -m pytest
  - Explicit live smoke with PIKO_ENABLE_LLM_WRITER=true and PIKO_LIVE_LLM_TEST=true
  - rg -n "sk-proj|Incorrect API key|OPENAI_API_KEY|Authorization: Bearer|Bearer sk-" .piko artifacts packages tests docs
- Results:
  - Targeted tests: 12 passed, 2 skipped in 0.22s
  - Full pytest: 73 passed, 3 skipped in 0.85s
  - Article pipeline: status=completed, writer_llm_used=False, real_collection_performed=False, verification_status=pass, publishing_performed=False
  - Live smoke: real request attempted; HTTP 401; fallback used; artifact stayed unpublished and verification_report.status=pass
  - Sensitive scan: no API key or OpenAI error body persisted; matches are limited to environment variable names and documentation placeholders.
- Failures:
  - Live LLM generation did not complete because the available OPENAI_API_KEY was rejected with HTTP 401. This is recorded as a fallback success, not as accepted LLM output.

## Direction Check
- Player need: still scoped to Stardew Valley save file location benchmark.
- Source evidence: LLM path consumes only existing evidence cards and ranked steps.
- Structured judgment: RankingAgent output remains the step source; LLM does not rank or extract evidence.
- Clear guide output: WriterAgent can draft from structured inputs; EditorAgent still runs afterward.
- Traceable sources: claim_trace, source_ids, evidence_card_ids, factcheck output, and verification_report remain present.
- Risk warnings: publish_ready=false and publishing_performed=false are preserved; risky save-file actions keep backup warnings.

## Prohibited Items Check
- Real external API: only one explicit OpenAI live smoke attempt; default pytest and workflow stayed offline for LLM.
- Real crawler: not added.
- LLM source finding: not added.
- LLM evidence extraction: not added.
- LLM final factcheck: not added.
- Raw full source text in prompt: blocked by prompt sanitizer and bounded payload construction.
- Real publishing: not added; publishing_performed=false.
- Deploy: not performed.
- Git commit: not performed.
- Admin review / human approval: not added.
- Verification bypass: not added.

## Risks And Notes
- Unfinished:
  - No successful LLM-authored draft was produced because the available API key returned HTTP 401.
- Risks:
  - Piko-verify should inspect the prompt payload sanitizer and confirm it excludes raw_text and sensitive field names.
  - Piko-verify should inspect the fallback artifact and confirm HTTP error storage is non-sensitive.
  - Future successful live LLM output should be reviewed carefully for unsupported claims and source trace completeness.
- Assumptions:
  - The LLM adapter remains a writer-only pilot and should not expand into source discovery, evidence extraction, ranking, final factcheck, publishing, or deployment.

## Next Recommendation
- Suggested next round: Piko-verify LLM Writer Live Pilot verification.
- Why: verify default-off behavior, mock LLM trace checks, failed live smoke fallback, and artifact safety before any future successful live LLM drafting attempt.
