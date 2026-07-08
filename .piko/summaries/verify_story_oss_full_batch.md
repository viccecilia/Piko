# STORY + OSS Full Batch Verification Summary

Verification result: failed

Verified scope: STORY-plus-OSS-full-batch

Verified by: Piko-verify

Verified at: 2026-07-02T10:14:17.4386100+09:00

## Validations Run

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`: passed
- `python -m pytest tests\test_discovery_search.py -q`: 69 passed
- `python -m pytest`: 161 passed, 3 skipped
- `python -m packages.storytelling.story_package --verify`: passed
- `python -m packages.oss_learning.domain_registry --domain gaming`: passed
- `python -m packages.oss_learning.domain_registry --domain ai_tools`: passed
- `python -m packages.oss_learning.domain_registry --domain unknown`: returned safe failed candidate-only response
- STORY JSON parse probes: passed
- STORY text/HTML presence probes: passed for required artifacts
- OSS JSON parse probes: passed
- API probes:
  - `/discovery/domain-probe?domain=gaming`: 200, candidate-only, publish-ready false
  - `/discovery/domain-probe?domain=ai_tools`: 200, candidate-only, publish-ready false
  - `/discovery/domain-probe?domain=unknown`: 200, safe failed response, candidate-only, publish-ready false
- Guardrail scan over STORY/OSS artifacts, packages, tests, docs, and discovery API route: found one blocking issue

## STORY Integrity Check

Passed.

All required STORY round and stage summaries are present:

- STORY-0: `worker_STORY-0-R01.md`, `worker_STORY-0-R02.md`, `worker_STORY-0.md`
- STORY-1: `worker_STORY-1-R01.md`, `worker_STORY-1-R02.md`, `worker_STORY-1.md`
- STORY-2: `worker_STORY-2-R01.md`, `worker_STORY-2-R02.md`, `worker_STORY-2-R03.md`, `worker_STORY-2.md`
- STORY-3: `worker_STORY-3-R01.md`, `worker_STORY-3-R02.md`, `worker_STORY-3-R03.md`, `worker_STORY-3.md`
- STORY-4: `worker_STORY-4-R01.md`, `worker_STORY-4-R02.md`, `worker_STORY-4.md`
- Batch summary: `worker_storytelling_content_batch.md`

## STORY Artifact Check

Mostly passed, with one blocking guardrail issue.

Required artifacts are present:

- `artifacts/storytelling/template_registry.json`
- `artifacts/storytelling/latest_candidate_selection.json`
- `artifacts/storytelling/latest_copy_package.json`
- `artifacts/storytelling/latest_wechat_article.md`
- `artifacts/storytelling/latest_xiaohongshu.md`
- `artifacts/storytelling/latest_voiceover.md`
- `artifacts/storytelling/latest_tts_plan.json`
- `artifacts/storytelling/latest_storyboard.md`
- `artifacts/storytelling/latest_video/index.html`

Required safety checks passed:

- `latest_copy_package.json`: `publish_ready=false`, `publishing_performed=false`
- `latest_tts_plan.json`: `voice_cloning=false`, `specific_real_person_voice=false`
- `template_registry.json`: exactly one active template, `agent-skill-storytelling:v1`
- `python -m packages.storytelling.story_package --verify`: `status=passed`

Blocking issue:

- `artifacts/storytelling/piko-skill-radar-demo/index.html` is a STORY artifact from this worker batch and contains an external script dependency:
  - `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`
- This violates the full-batch guardrail `no default network` because opening the local HTML can perform an external network request by default.
- The required `latest_video/index.html` artifact itself passed the local/internal checks, but the broader generated STORY artifact set still contains this external dependency.

## OSS Integrity Check

Passed.

All required OSS round and stage summaries are present:

- OSS-1: `worker_OSS-1-R01.md`, `worker_OSS-1-R02.md`, `worker_OSS-1-R03.md`, `worker_OSS-1.md`
- OSS-2: `worker_OSS-2-R01.md`, `worker_OSS-2-R02.md`, `worker_OSS-2.md`
- OSS-3: `worker_OSS-3-R01.md`, `worker_OSS-3-R02.md`, `worker_OSS-3-R03.md`, `worker_OSS-3.md`
- OSS-4: `worker_OSS-4-R01.md`, `worker_OSS-4-R02.md`, `worker_OSS-4-R03.md`, `worker_OSS-4.md`
- OSS-5: `worker_OSS-5-R01.md`, `worker_OSS-5-R02.md`, `worker_OSS-5.md`
- Batch summary: `worker_OSS-1-to-OSS-5.md`

## OSS Proposal-Only Check

Passed.

Required OSS artifacts are present and JSON-parseable:

- `artifacts/oss_research/latest_ranked_projects.json`
- `artifacts/oss_research/latest_patterns.json`
- `artifacts/oss_research/latest_upgrade_proposals.json`
- `artifacts/oss_research/agent_framework_adapter_proposal.json`
- `artifacts/oss_research/domain_plugin_proposal.json`
- `artifacts/oss_research/capability_handoff_candidates.json`
- `artifacts/oss_research/latest_cap_queue_candidates.json`
- `artifacts/oss_research/latest_story_queue_candidates.json`

OSS checks passed:

- No auto-apply markers were true.
- `latest_ranked_projects.json` reports `auto_apply_performed=false`.
- `latest_upgrade_proposals.json` keeps proposals with `auto_apply_allowed=false`.
- `latest_story_queue_candidates.json` keeps `auto_publish=false`.
- Domain registry/API responses remain candidate-only.
- No vendored repository directory or copied third-party source was found in the OSS artifact/package structure.
- `raw_repository_body`, `full_readme`, `api_key`, and `authorization` appear only as prohibited-field declarations in the intake schema, not as retained data.

## API / Domain Probe Check

Passed.

- `/discovery/domain-probe?domain=gaming`: `status=completed`, `candidate_only=true`, `publish_ready=false`
- `/discovery/domain-probe?domain=ai_tools`: `status=completed`, `candidate_only=true`, `publish_ready=false`
- `/discovery/domain-probe?domain=unknown`: `status=failed`, `error=unknown_domain`, `candidate_only=true`, `publish_ready=false`

## Guardrail Check

Failed due to one blocking issue.

Passed guardrails:

- No publish/upload/deploy behavior was executed.
- No commit/push occurred; the workspace is not a Git repository.
- No default LLM call was found.
- No voice cloning or specific real-person voice request was found.
- No unauthorized external image dependency was found in the required `latest_video/index.html`.
- No secrets, API keys, or authorization headers were retained as data in required STORY/OSS artifacts.
- No raw copied article or vendored external source repository was found.
- No verification bypass or Gate relaxation was found.
- No active skill/capability/template replacement was found; active STORY template remains `agent-skill-storytelling:v1`.

Failed guardrail:

- `no default network`: `artifacts/storytelling/piko-skill-radar-demo/index.html` references `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`.

## Findings

Blocking:

- STORY artifact `artifacts/storytelling/piko-skill-radar-demo/index.html` contains an external CDN dependency. This conflicts with the full-batch no-default-network requirement.

Non-blocking note:

- `round_status.json` still pointed `verification_prompt_file` to `.piko/round_queue/STORY-BATCH-VERIFY.md`. This was not treated as blocking because this verification explicitly covered STORY + OSS full batch. The status should point to this full-batch verification summary after the worker fixes the blocking issue.

## Required Rework

Return to `STORY-plus-OSS-full-batch` and fix the generated STORY artifact surface:

- Remove the external CDN script from `artifacts/storytelling/piko-skill-radar-demo/index.html`, or replace it with a local/internal/no-network implementation.
- Add or update a STORY artifact test that scans generated HTML for `http://` and `https://` dependencies unless explicitly whitelisted as non-executed source notes.
- Re-run:
  - `python -m pytest tests\test_storytelling_artifacts.py -q`
  - `python -m pytest`
  - STORY/OSS guardrail scan
- Keep all artifacts internal, unpublished, and candidate-only.
