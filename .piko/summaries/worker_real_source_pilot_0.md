# Worker Summary: real-source-pilot-0

## Round
- Round ID: real-source-pilot-0
- Round Name: Real Source Pilot 0 - PCGamingWiki / MediaWiki Controlled Pilot
- Stage: Real Source Pilot
- Started from next_round: null after post-S8-stabilization verified passed

## Scope
- Allowed files touched: packages/collectors/mediawiki.py, packages/collectors/pcgamingwiki.py, packages/collectors/base.py, packages/shared/schemas.py, docs/current_state.md, docs/source_policy.md, tests/test_stage_5.py
- Files intentionally not touched: workflow source collection logic, real publishing paths, admin review paths, Reddit/Steam/Google/ProtonDB connectors, deployment files
- Upstream fixes made: none beyond connector safety and source metadata normalization for the controlled pilot

## Changes
- Modified files:
  - packages/collectors/base.py
  - packages/collectors/mediawiki.py
  - packages/collectors/pcgamingwiki.py
  - packages/shared/schemas.py
  - tests/test_stage_5.py
  - docs/current_state.md
  - docs/source_policy.md
- Added files:
  - .piko/summaries/worker_real_source_pilot_0.md
- Deleted files: none
- Behavioral changes:
  - ConnectorSearchResult now includes retrieved_at.
  - SourceReference can carry retrieved_at when connector output is normalized into source metadata.
  - MediaWiki search clamps result limit to 1..10.
  - MediaWiki normalized results now explicitly mark raw_text_included=false and keep raw_text empty.
  - PCGamingWiki now emits pcgamingwiki source_type and pcgamingwiki_* source_id values instead of inheriting mediawiki identity.
  - Default connector behavior remains disabled unless PIKO_ENABLE_REAL_CONNECTORS=true.

## Task Status
- 执行任务: completed
- 测试任务: completed
- 协作验收任务: ready for Piko-verify

## Verification Run By Worker
- Commands run:
  - python -m pytest
  - python -m packages.workflows.article_pipeline
- Results:
  - python -m pytest: 52 passed in 0.67s
  - python -m packages.workflows.article_pipeline: completed structured mock workflow JSON; verification_report.status=pass; publish_action=draft_review; publish_decision.value=verified_candidate; real_collection_performed=false
- Failures:
  - none

## Sample Output
```json
{
  "connector_default": {
    "PIKO_ENABLE_REAL_CONNECTORS": false,
    "search_without_opt_in": "DisabledConnectorError"
  },
  "mocked_pcgamingwiki_result": {
    "source_id": "pcgamingwiki_456",
    "source_type": "pcgamingwiki",
    "url": "https://www.pcgamingwiki.com/w/api.php?curid=456",
    "title": "Example Game",
    "retrieved_at": "datetime",
    "trust_tier": "reference",
    "clean_text": "Settings and launch notes",
    "raw_text": null,
    "metadata": {
      "pageid": "456",
      "raw_text_included": false
    }
  },
  "mocked_mediawiki_request": {
    "user_agent": "PikoBot/0.1 source-policy-contact-required",
    "timeout_seconds": 5.0,
    "requested_limit": 50,
    "sent_srlimit": 10
  }
}
```

## Direction Check
- Player need: unchanged; workflow still starts from a player question and local mock fixtures by default.
- Source evidence: connector output now has stronger source metadata for future evidence ingestion.
- Structured judgment: connector results remain Pydantic models and can be normalized into SourceReference.
- Clear guide output: no guide generation behavior changed.
- Traceable sources: source_id, source_type, URL, title, retrieved_at, and trust_tier are present on pilot connector records.
- Risk warnings: docs continue to require opt-in, mocked tests, bounded result limits, and no raw page dumps in workflow.

## Prohibited Items Check
- Real external API: not used in tests or default paths; connector remains disabled by default.
- Real crawler: not added.
- Real publishing: not added.
- Admin review / human approval: not added.
- Unsourced claims: no real content claims added; tests use synthetic mocked HTTP responses.
- Other connectors: Reddit, Steam, Google, and ProtonDB were not connected.

## Risks And Notes
- Unfinished: no manual live request was performed; that is intentionally deferred to the next round.
- Risks: MediaWiki _default_http_get still contains urlopen for future opt-in use, so Piko-verify should confirm every default/test path stays blocked or mocked.
- Assumptions: PCGamingWiki remains represented as a MediaWiki API specialization, not a crawler.

## Next Recommendation
- Suggested next round: Piko-verify for real-source-pilot-0.
- Why: confirm connector safety boundaries, mock-only tests, normalized source metadata, and no accidental network/publish/admin-review behavior before any manual opt-in single real request.
