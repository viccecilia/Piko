# Current State

Piko is currently a mock-first, source-based game guide platform skeleton. It is stable enough for local verification and for planning real source governance, but it is not a production publishing system.

## What Piko Has Today

- FastAPI API with health, registry, workflow, verification, eligibility, and feedback endpoints.
- Agent Registry with deterministic placeholder agents.
- Tool Registry with mock tools.
- Local source fixtures for a launch/crash issue.
- Source selection over local fixtures.
- Evidence card extraction with source IDs, confidence, snippets, and risk notes.
- Article brief generation from player need, sources, evidence, conflicts, and ranked steps.
- Deterministic draft output matching the Piko article template.
- Optional LLM writer adapter interface, disabled by default and limited to WriterAgent draft generation from structured evidence.
- Readability, risk, evidence, conflict, fact-check, and publish gates.
- Workflow-level verification reports.
- Publishing eligibility checks that never deploy.
- In-memory evidence index and structured memory store.
- Disabled-by-default connector interface with mocked connector tests.
- PCGamingWiki/MediaWiki connector pilot code that normalizes mocked HTTP responses into source records.
- Explicit opt-in PCGamingWiki/MediaWiki source-candidate path that can turn normalized source records into traceable evidence cards.
- Public guide template with mock source-backed content.
- Feedback endpoint that stores feedback as a verification/refresh signal only.
- Operations notes for deployment, backup, restore, and rollback planning.
- Planning-only self-improvement modules for diagnostics, upgrade proposals, patch plans, regression plans, and ledger entries.
- Topic discovery search over fixture-backed player question signals, with scoring, lifecycle, actionability, source coverage, region signals, competition gap, watchlist states, API filters, and CLI filters.
- Topic discovery real-source pilot contract for PCGamingWiki/MediaWiki metadata, disabled by default and fixture-backed for ordinary verification.

## What Is Still Mock-First

- Source data comes from local fixtures by default.
- Agents are deterministic placeholders, not real model-backed agents.
- WriterAgent remains rule-based by default; the LLM writer path requires explicit local opt-in and is not used by ordinary tests.
- Evidence extraction is rule-based.
- Indexing and memory are in-memory.
- Web output is a static guide template.
- Monitoring uses estimates, not production telemetry or billing APIs.
- MediaWiki/PCGamingWiki connector code exists only behind explicit opt-in.
- PCGamingWiki/MediaWiki connector tests use mocked HTTP by default; the single live smoke test is skipped unless explicitly enabled.
- Real source records can enter the evidence chain as low-confidence source candidates, but they do not become player-facing recommendations until page-level evidence extraction exists.
- Topic discovery output is still a prioritization signal. It can produce article candidates and source-query hints, but it does not trigger collection, draft generation, publishing, deployment, or LLM calls.

## Dangerous Behaviors Disabled By Default

- No real external API calls in default/test paths.
- No crawlers or scraping jobs.
- No real publishing.
- No deployment.
- No admin review queue or human approval backend.
- No feedback-driven automatic article edits.
- No self-improvement-driven automatic patching, commits, deployment, publishing, or verification bypass.
- No LLM calls unless `PIKO_ENABLE_LLM_WRITER=true`; live smoke also requires `PIKO_LIVE_LLM_TEST=true` and `OPENAI_API_KEY`.

## Run The API

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m uvicorn apps.api.main:app --reload
```

Health check:

```text
GET http://127.0.0.1:8000/health
```

Verification window:

```text
GET http://127.0.0.1:8000/verification/window
```

## Run The Workflow

CLI:

```powershell
python -m packages.workflows.article_pipeline
```

API:

```text
POST /workflow/article/run
```

Example body:

```json
{
  "game_id": "game_mock_001",
  "game_name": "Example Game",
  "player_question": "crash on startup"
}
```

## Run Verification

Run tests:

```powershell
python -m pytest
```

Run verification endpoint with a workflow report:

```text
POST /workflow/article/verify
```

The workflow response already includes:

- `verification_report`
- `pipeline_state.verification_report`
- `publish_decision`
- `pipeline_state.monitoring_summary`

## Run Topic Discovery

CLI:

```powershell
python -m packages.discovery.search_cli --min-game-heat 50 --limit 5
python -m packages.discovery.search_cli --decision publish_candidate --intent save_file --lifecycle resolved --actionability single_page_answerable --min-opportunity 80 --limit 3
python -m packages.discovery.search_cli --decision watchlist_waiting_for_answer --intent bug_fix --view summary --limit 3
```

API:

```text
POST /discovery/search
GET /discovery/window
POST /discovery/report
```

Discovery returns topic clusters, watchlist candidates, article-candidate handoff hints, and retrospective signals. It must keep:

- `real_collection_performed=false` in default paths
- `publish_ready=false` for candidates
- `requires_evidence_pipeline=true` before any article workflow handoff

Discovery does not publish, deploy, run the article pipeline, call LLMs, or fetch real community data by default.

## Real Market Discovery Status

Real Market Discovery now has controlled contracts for Steam, Reddit,
SERP/search snippets, JP community, and KR community market signals.
The default mode is still fixture/offline.

Useful commands:

```powershell
python -m packages.discovery.search_cli --min-game-heat 50 --limit 5
python -m packages.discovery.real_market_live_smoke --query "Stardew Valley" --limit-per-source 3
```

The live smoke command is skip-first. It requires both:

```powershell
$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE = "true"
$env:PIKO_LIVE_DISCOVERY_TEST = "true"
```

and at least one configured endpoint such as:

```powershell
$env:PIKO_STEAM_DISCOVERY_URL = "https://approved-json-endpoint.example/steam"
```

Without flags or endpoints, it returns `status=skipped` and performs no
request. This is the expected local state unless an operator intentionally
configures a bounded test endpoint.

Ranking surfaces:

- `GET /discovery/rankings?limit=5`
- `GET /discovery/window`

They expose hot games, guide-need buckets, watchlist topics, conflict topics,
and high-risk blocked topics. These are prioritization signals only. They do
not publish and do not mark anything as article-ready.

The RM-4 candidate pilot can write an internal draft artifact for the highest
safe `publish_candidate`, or use a mocked equivalent when live endpoints are
absent. It keeps `publish_ready=false`, `publishing_performed=false`, and a
verification report.

## Topic Discovery To DA Handoff

Topic Discovery Strengthening closes at TD-8 and resumes the paused DA queue at `DA-3-R01`.

The handoff from TD to DA is candidate-only:

- `publish_candidate` clusters may become DA input for deeper evidence analysis.
- `watchlist_waiting_for_answer` clusters stay monitoring candidates until stronger answer/evidence signals appear.
- `conflict_explainer` clusters require synthesis and uncertainty handling, not a single-answer guide.
- `blocked_high_risk` clusters must not enter normal guide generation.

DA should treat TD output as prioritization metadata and source-query hints, not as publishing approval.

## Optional LLM Writer Pilot

The LLM writer pilot is disabled by default. It is limited to WriterAgent and must only use already-structured inputs:

- player question
- game
- article intent
- evidence cards
- ranked steps
- source IDs
- allowed short snippets already present on evidence cards
- risk notes
- uncertainty notes

Do not pass raw full source text, credentials, API keys, authorization headers, long webpage bodies, or unbounded source dumps into the LLM prompt.

Manual live smoke opt-in requires:

```powershell
$env:PIKO_ENABLE_LLM_WRITER = "true"
$env:PIKO_LIVE_LLM_TEST = "true"
$env:OPENAI_API_KEY = "<set outside repository>"
```

If the adapter is disabled, missing a key, or fails, WriterAgent falls back to the rule-based writer and records the fallback status. LLM output still goes through EditorAgent, FactcheckAgent, and verification mirrors. It must remain `publish_ready=false` and `publishing_performed=false`.

## Publishing Eligibility

Use:

```text
POST /workflow/article/eligibility
```

Eligibility can return an eligible candidate, but it never deploys. `deploy_performed` must remain `false`.

## Connector Opt-In

Real connectors are disabled unless:

```text
PIKO_ENABLE_REAL_CONNECTORS=true
```

For the current PCGamingWiki/MediaWiki pilot, manual opt-in is intentionally a local, single-operator action:

```powershell
$env:PIKO_ENABLE_REAL_CONNECTORS = "true"
```

The live connector smoke also requires:

```powershell
$env:PIKO_LIVE_CONNECTOR_TEST = "true"
```

Leave both variables unset or set to `false` for normal development and tests. The connector must send a Piko user agent, use a timeout, clamp result limits, and return source metadata (`source_id`, `source_type`, `url`, `title`, `retrieved_at`, `trust_tier`) instead of long raw page dumps.

When enabled for the current pilot, PCGamingWiki/MediaWiki records may produce `source_candidate` evidence cards. Those cards preserve `source_id` traceability and mark `needs_more_evidence`; they are not enough to produce publish-ready guide steps.

Before enabling this outside a controlled manual trial, Piko needs source governance, rate limits, source-specific policy checks, and mocked tests for every connector behavior.

## Connector Registry

Piko now has a domain-agnostic connector registry contract for candidate connectors across domain packs. The registry uses neutral concepts such as `domain_id`, `source_type`, `retained_fields`, `permission_boundary`, and `collection_mode`; gaming and AI-tools source details live in their domain connector packs rather than core workflow code.

Current connector artifacts are generated under `artifacts/connector_registry/`:

- `connector_registry_contract.json`
- `connector_manifest_examples.json`
- `source_governance_policy.json`
- `credential_policy.json`
- `permission_audit_policy.json`
- `gaming_connector_pack.json`
- `ai_tools_connector_pack.json`
- `connector_routing.json`
- `collection_plan.json`
- `collection_dry_run_report.json`
- `operator_connector_surface.json`

All connectors default to `candidate`, `disabled`, and `dry_run`. Collection plans keep `real_collection_performed=false` unless a future operator explicitly approves live collection and supplies required endpoint or credential policy. Missing REAL approved endpoint configuration is represented as `blocked_for_endpoint`; it is not treated as a successful live run.

Read-only operator/API surfaces:

```text
GET /connectors
GET /connectors/window
GET /connectors/route?domain_id=gaming&source_type=market
POST /connectors/plan?domain_id=gaming&target_need=save file location
```

These surfaces do not fetch live data, do not call LLMs, do not publish, and do not store raw/full source bodies, credentials, tokens, cookies, API keys, or authorization headers.

## LIVE-CONNECTOR Pilot

The LIVE-CONNECTOR pilot is the first controlled bridge from the connector registry toward a bounded live probe. It can only select `approved_json_endpoint`; Steam, Reddit, JP/KR community, SERP, MediaWiki, crawler, and HTML scrape paths remain excluded.

Artifacts are written under `artifacts/live_connector_pilot/`:

- `live_connector_selection.json`
- `live_connector_approval.json`
- `endpoint_readiness.json`
- `bounded_endpoint_verification.json`
- `bounded_live_collection.json`
- `normalized_live_signals.json`
- `connector_registry_feedback.json`
- `real_funnel_handoff.json`
- `candidate_only_ranking_preview.json`
- `operator_live_connector_surface.json`

Default local state is `blocked_for_endpoint`. A bounded live probe requires all three settings:

```powershell
$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE = "true"
$env:PIKO_LIVE_DISCOVERY_TEST = "true"
$env:PIKO_APPROVED_ENDPOINT_URL = "<approved JSON endpoint>"
```

If any value is missing, no request is made and `real_collection_performed=false`. If a configured endpoint returns invalid payload shape, the pilot must report `failed_contract_validation`. A successful probe may normalize bounded metadata/signals into REAL funnel handoff artifacts, but it still keeps `publish_ready=false`, `publishing_performed=false`, and `candidate_only=true`.

Read-only operator/API surfaces:

```text
GET /connectors/live
GET /connectors/live-window
```

## Local Approved Endpoint Success Path

Piko also has a local approved endpoint success path for verifying the connector and REAL funnel wiring without depending on an external provider. This uses the existing approved endpoint fixture through a temporary localhost JSON endpoint. It proves `real_collection_performed=true` only for:

```text
scope=local_approved_endpoint
broad_internet_coverage=false
```

It is not broad internet coverage, not Steam/Reddit/JP/KR/SERP live collection, and not crawler output. The opt-in environment is applied only inside the test/runner process and is restored afterward.

Commands and surfaces:

```powershell
python -m packages.local_endpoint.pipeline --smoke
```

```text
GET /local-endpoint/approved-json
GET /local-endpoint/result
GET /local-endpoint/window
```

Generated artifacts live under `artifacts/local_endpoint/` and include contract validation, fixture safety, local endpoint smoke, live connector success, normalized signals, REAL funnel handoff, internal article handoff, and operator result. They must keep `publish_ready=false`, `publishing_performed=false`, `raw_response_body_saved=false`, and `broad_internet_coverage=false`.

## External Approved Endpoint Pilot

The EXTERNAL-ENDPOINT pilot is separate from the local approved endpoint success path. It is for a real operator-approved external JSON endpoint only, with this success scope:

```text
scope=external_approved_endpoint
broad_internet_coverage=false
```

It requires all of:

```powershell
$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE = "true"
$env:PIKO_LIVE_DISCOVERY_TEST = "true"
$env:PIKO_APPROVED_ENDPOINT_URL = "<external approved JSON endpoint>"
```

The external pilot rejects localhost, file, fixture, raw-body, HTML, RSS, and crawler-style endpoints as external success. If the URL or opt-in is missing, status is `blocked_for_external_endpoint`. If the JSON contract is invalid, status is `failed_contract_validation`. A success can generate external normalized signals, REAL funnel handoff, and an internal candidate article package, but it must not claim broad internet coverage and must keep `publish_ready=false` and `publishing_performed=false`.

Read-only operator/API surfaces:

```text
GET /external-endpoint/result
GET /external-endpoint/window
```

## Source Provider Package

SOURCE-PROVIDER prepares a deploy-ready static JSON package for an operator-owned external approved endpoint. It does not upload, deploy, publish, crawl, scrape HTML, call an LLM, or store credentials. The package is written to:

```text
artifacts/source_provider/static_endpoint_package/approved-market.json
artifacts/source_provider/static_endpoint_package/README.md
```

The package payload conforms to the approved endpoint contract and is candidate-only. Localhost, `127.0.0.1`, `file`, and fixture URLs are not valid external endpoints. If no external URL is configured, the provider status is `deploy_ready_pending_host`, with `external_provider_validated=false` and `real_collection_performed=false`.

Read-only operator/API surfaces:

```text
GET /source-provider/result
GET /source-provider/window
```

After the operator hosts the JSON at a non-local HTTP(S) URL, rerun validation with:

```powershell
$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE = "true"
$env:PIKO_LIVE_DISCOVERY_TEST = "true"
$env:PIKO_APPROVED_ENDPOINT_URL = "<external approved JSON endpoint>"
python -m packages.source_provider.pipeline --write-artifacts
```

Only a non-local HTTP(S) URL fetch with a passing contract validation can set `external_provider_validated=true`. That does not imply broad internet coverage; it only prepares the next EXTERNAL-ENDPOINT rerun.

## Before Real Source Integration

- Confirm source policy for each source.
- Add rate limits and retry rules.
- Add user-agent/contact policy.
- Keep connectors disabled by default.
- Store raw and clean text separately.
- Preserve `source_id` on every evidence card and ranked step.
- Ensure verification fails missing evidence, source mismatches, risky recommendations, and publish-ready decisions with failed gates.
- Confirm no public publishing path exists until a dedicated publishing round.
## Real Endpoint Verification REV-3 To REV-6

Piko now has an internal, controlled Real Endpoint Verification surface for approved JSON endpoint data:

- Approved source registry: `/discovery/endpoint-registry`
- Safe endpoint adapter preview: `/discovery/endpoint-search`
- Endpoint-fed ranking preview: `/discovery/endpoint-rankings`
- Funnel trace and window: `/discovery/funnel-trace`, `/discovery/funnel-window`
- Latest funnel report: `/discovery/funnel-report`
- Source hints/readiness: `/discovery/source-hints`
- Internal article package: `/discovery/article-package`
- Publish readiness metadata: `/discovery/publish-readiness`
- Operator result surface: `/discovery/operator-result`

These surfaces are internal and candidate-only. Fixture and mock-live modes do not perform live collection. Live endpoint verification still requires explicit opt-in flags and an approved JSON endpoint URL.

Generated REV artifacts:

- `artifacts/discovery_reports/latest_real_market_funnel_report.json`
- `artifacts/article_drafts/latest_source_backed_article_package.json`
- `artifacts/article_drafts/latest_source_backed_article_package.md`
- `artifacts/publish_readiness/latest_publish_readiness.json`

All generated REV artifacts must keep `publish_ready=false`, `publishing_performed=false`, and candidate-only safety metadata. They must not store raw response bodies, full posts, full pages, full comments, images, maps, copied tables, credentials, API keys, authorization headers, secrets, or crawler output.

## LIVE-1 Approved Endpoint Smoke

LIVE-1 verifies whether one approved JSON endpoint is ready for a bounded live smoke. A real request only runs when all of these are configured:

- `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
- `PIKO_LIVE_DISCOVERY_TEST=true`
- `PIKO_APPROVED_ENDPOINT_URL=<approved-json-endpoint>`

If any setting is missing, `python -m packages.discovery.real_endpoint_verify --live --write-artifact` returns `status=skipped`, keeps `real_collection_performed=false`, and writes the skipped reason to `artifacts/endpoint_verification/latest_endpoint_verification.json`. The operator result surface mirrors this status under `live_endpoint_verification`.
## V03 Practical Plugin Absorption

V03 adds a LangGraph-style workflow adapter pilot as a local deterministic fixture. It covers workflow nodes, state transfer, Gate decisions, retry/failure semantics, trace output, and internal article package handoff. No LangGraph package is installed, no external dependency is vendored, no active runtime is replaced, and all real activation remains blocked behind human approval and Piko-verify.
## V04 Real LangGraph Backend Approval Pilot

V04 adds a controlled real LangGraph backend approval pilot. It creates approval, dependency review, backend selector, smoke, operator status, and readiness artifacts. Current backend status is `available_for_pilot_smoke` with effective backend `langgraph_backend`. Production activation remains `not_approved_for_production`, active runtime is not replaced, and local_fixture remains the default fallback.
## V05 Real LangGraph Install Smoke

V05 explicitly approved and attempted a real LangGraph install/import smoke. Install status is `already_available`, import success is `True`, version is `unknown`, minimal smoke is `success`, and workflow smoke is `success` using effective backend `langgraph_backend`. Production activation remains false, active runtime is not replaced, and no real data batch was started.
