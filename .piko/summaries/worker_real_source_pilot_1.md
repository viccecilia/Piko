# Worker Summary: real-source-pilot-1

## Round
- Round ID: real-source-pilot-1
- Round Name: Real Source Pilot 1 - PCGamingWiki / MediaWiki Single-Source Live Smoke
- Stage: Real Source Pilot
- Started from next_round: null after real-source-pilot-0 verified passed

## Scope
- Allowed files touched: packages/shared/config.py, packages/collectors/mediawiki.py, docs/current_state.md, docs/source_policy.md, tests/test_stage_5.py, .piko/summaries/*
- Files intentionally not touched: article workflow source-agent behavior, publishing code, admin review code, deployment code, Reddit/Steam/Google/ProtonDB connectors
- Upstream fixes made: added the explicit live connector test switch needed for controlled real-network execution

## Changes
- Modified files:
  - packages/shared/config.py
  - packages/collectors/mediawiki.py
  - tests/test_stage_5.py
  - docs/current_state.md
  - docs/source_policy.md
- Added files:
  - .piko/summaries/real_source_pilot_1_sample.json
  - .piko/summaries/worker_real_source_pilot_1.md
- Deleted files: none
- Behavioral changes:
  - Added `PIKO_LIVE_CONNECTOR_TEST` / `Settings.live_connector_test`, defaulting to false.
  - Added a live PCGamingWiki/MediaWiki smoke test that is skipped unless both `PIKO_ENABLE_REAL_CONNECTORS=true` and `PIKO_LIVE_CONNECTOR_TEST=true`.
  - MediaWiki snippets are lightly cleaned and clamped to 500 characters.
  - Ordinary pytest remains offline by default.

## Task Status
- 执行任务: completed
- 测试任务: completed
- 协作验收任务: ready for Piko-verify

## Real Request
- Did a real request happen: yes
- Source: PCGamingWiki public MediaWiki API
- API target: `https://www.pcgamingwiki.com/w/api.php?action=query&list=search&srsearch=Hades&format=json&srlimit=3`
- Query: `Hades`
- Player question context: `Where is the save file location?`
- Result limit: 3
- User-Agent: configured Piko user agent
- Timeout: configured connector timeout
- First attempt note: `Hades save file location` returned zero search results; the controlled live smoke was narrowed to the game query `Hades`, which returned normalized records.

## Normalized Source Records
Saved sample: `.piko/summaries/real_source_pilot_1_sample.json`

```json
{
  "source": "pcgamingwiki_mediawiki_api",
  "query": "Hades",
  "player_question": "Where is the save file location?",
  "result_count": 3,
  "records": [
    {
      "source_id": "pcgamingwiki_183626",
      "source_type": "pcgamingwiki",
      "url": "https://www.pcgamingwiki.com/w/api.php?curid=183626",
      "title": "Hades II",
      "retrieved_at": "2026-06-21T06:29:21.357559Z",
      "trust_tier": "reference",
      "raw_text": null,
      "metadata": {
        "pageid": "183626",
        "raw_text_included": false
      }
    },
    {
      "source_id": "pcgamingwiki_137191",
      "source_type": "pcgamingwiki",
      "url": "https://www.pcgamingwiki.com/w/api.php?curid=137191",
      "title": "Hades",
      "retrieved_at": "2026-06-21T06:29:21.357559Z",
      "trust_tier": "reference",
      "raw_text": null,
      "metadata": {
        "pageid": "137191",
        "raw_text_included": false
      }
    },
    {
      "source_id": "pcgamingwiki_91106",
      "source_type": "pcgamingwiki",
      "url": "https://www.pcgamingwiki.com/w/api.php?curid=91106",
      "title": "The Road to Hades",
      "retrieved_at": "2026-06-21T06:29:21.357559Z",
      "trust_tier": "reference",
      "raw_text": null,
      "metadata": {
        "pageid": "91106",
        "raw_text_included": false
      }
    }
  ]
}
```

## Verification Run By Worker
- Commands run:
  - `python -m pytest`
  - `python -m packages.workflows.article_pipeline`
  - `$env:PIKO_ENABLE_REAL_CONNECTORS = 'true'; $env:PIKO_LIVE_CONNECTOR_TEST = 'true'; python -m pytest tests/test_stage_5.py -k live_pcgamingwiki_mediawiki_smoke -q`
  - `$env:PIKO_ENABLE_REAL_CONNECTORS = 'true'; $env:PIKO_LIVE_CONNECTOR_TEST = 'true'; python -c "... PCGamingWikiConnector().search('Hades', limit=3) ..."`
- Results:
  - `python -m pytest`: 52 passed, 1 skipped in 0.82s. The skipped test is the live connector smoke, proving ordinary pytest remains offline by default.
  - `python -m packages.workflows.article_pipeline`: completed mock workflow; `real_collection_performed=false`; `verification_report.status=pass`; no publishing side effect.
  - Live smoke pytest command: 1 passed, 6 deselected in 1.10s.
  - Live sample command: returned 3 normalized source records and saved short metadata/snippet sample.
- Failures:
  - Initial live query `Hades save file location` returned 0 results, so the source search query was narrowed to `Hades` while keeping the player question context as save file location.

## Default / Offline Behavior
- Default `PIKO_ENABLE_REAL_CONNECTORS`: false
- Default `PIKO_LIVE_CONNECTOR_TEST`: false
- Ordinary pytest: offline, live smoke skipped
- Workflow default: local mock fixtures only, `real_collection_performed=false`
- Long raw page text: not saved; `raw_text=null` in live sample

## Direction Check
- Player need: save-file-location question is captured as context for the source pilot.
- Source evidence: one real source family was queried through a public MediaWiki API and normalized into source records.
- Structured judgment: records are Pydantic connector results and SourceReference-compatible metadata.
- Clear guide output: no guide or article was generated from the live source yet.
- Traceable sources: source IDs, source type, URLs, titles, retrieved_at, trust tier, and page IDs are present.
- Risk warnings: no risky player recommendation was generated; this round only produced source candidates.

## Prohibited Items Check
- Real external API: yes, explicitly for PCGamingWiki/MediaWiki live smoke only.
- Real crawler: not added; no HTML crawling or page-body scraping occurred.
- Real publishing: not added.
- Deployment: not added.
- Admin review / human approval: not added.
- Other connectors: Reddit, Steam, Google, and ProtonDB were not connected.
- Unsourced claims: no guide claims or player-facing recommendations were produced from live data.

## Risks And Notes
- Unfinished: live source candidates are not yet wired into evidence extraction or article workflow.
- Risks: MediaWiki search snippets can contain wiki markup; current cleaning removes HTML tags and clamps length but does not parse wiki templates.
- Assumptions: using a game-title query is the right first step before a later page-specific save-location extraction round.

## Next Recommendation
- Suggested next round: Piko-verify for real-source-pilot-1.
- Why: verify the double opt-in live test, ordinary offline pytest behavior, normalized source metadata, short sample storage, and no crawler/publishing/admin-review behavior before any source-to-evidence integration.
