# Worker Summary: real-source-pilot-2

## Round
- Round ID: real-source-pilot-2
- Round Name: Real Source Pilot 2 - Real Source Records Into Evidence Chain
- Stage: Real Source Pilot
- Started from next_round: null after real-source-pilot-1 verified passed

## Scope
- Allowed files touched: packages/agents/*, packages/indexing/evidence_extractor.py, packages/workflows/article_pipeline.py, packages/shared/schemas.py, docs/current_state.md, docs/source_policy.md, tests/*, .piko/summaries/*
- Files intentionally not touched: publishing/deployment code, admin review code, Reddit/Steam/Google/ProtonDB connectors, HTML crawlers, long raw-source storage
- Upstream fixes made: workflow now preserves source snippet/metadata and candidate evidence claim/risk note fields

## Changes
- Modified files:
  - packages/shared/schemas.py
  - packages/indexing/evidence_extractor.py
  - packages/agents/source_agent.py
  - packages/agents/evidence_agent.py
  - packages/agents/ranking_agent.py
  - packages/workflows/article_pipeline.py
  - docs/current_state.md
  - docs/source_policy.md
- Added files:
  - tests/test_real_source_pilot_2.py
  - .piko/summaries/real_source_pilot_2_chain_sample.json
  - .piko/summaries/worker_real_source_pilot_2.md
- Deleted files: none
- Behavioral changes:
  - `SourceReference` now preserves short `snippet`, `clean_text`, and metadata from normalized connector records.
  - Source Agent can use PCGamingWiki/MediaWiki normalized records only when both `PIKO_ENABLE_REAL_CONNECTORS=true` and `PIKO_LIVE_CONNECTOR_TEST=true`.
  - Evidence Agent can turn normalized source records into low-confidence `source_candidate` evidence cards with `source_id`.
  - Ranking Agent returns no ranked solution when evidence is only source-candidate level.
  - Workflow returns `needs_more_evidence` when no ranked answer-level steps exist.

## Real Source Into Evidence Chain
- Source: PCGamingWiki public MediaWiki API / normalized Pilot 1 records.
- Entry point: Source Agent returns normalized source candidates under explicit double opt-in.
- Evidence extraction: `extract_evidence_cards_from_source_records` creates source-candidate evidence cards from short snippet/clean_text and metadata.
- Traceability: each generated evidence card keeps the original `source_id`.
- Insufficient evidence behavior: no solution is invented; ranked steps remain empty and publish decision becomes `needs_more_evidence`.

## Sample Source Record
```json
{
  "source_id": "pcgamingwiki_137191",
  "source_type": "pcgamingwiki",
  "title": "Hades",
  "url": "https://www.pcgamingwiki.com/w/api.php?curid=137191",
  "retrieved_at": "2026-06-21T06:29:21.357559Z",
  "trust_tier": "reference",
  "raw_text_included": false
}
```

## Sample Evidence Card
```json
{
  "evidence_card_id": "ev_pcgamingwiki_137191_1_candidate",
  "source_id": "pcgamingwiki_137191",
  "claim_type": "source_candidate",
  "claim": "Hades is a pcgamingwiki source candidate for the player question.",
  "solution": null,
  "confidence": 35,
  "risk_note": "Source candidate only; needs page-level extraction before recommending an answer."
}
```

## Verification Report Traceability
- `source_evidence` checks at least one source exists.
- `evidence_source_trace` checks every evidence card source_id exists in workflow sources.
- Missing source_id coverage: offline test removes workflow sources after candidate evidence is generated; verification fails with missing source IDs.
- Insufficient real-source evidence coverage: offline test verifies candidate-only evidence yields `PublishDecisionValue.needs_more_evidence`, `blocks_publish=true`, empty ranked steps, and `publish_action=discard`.

## Verification Run By Worker
- Commands run:
  - `python -m pytest`
  - `python -m packages.workflows.article_pipeline`
  - `$env:PIKO_ENABLE_REAL_CONNECTORS = 'true'; $env:PIKO_LIVE_CONNECTOR_TEST = 'true'; python -m pytest tests/test_real_source_pilot_2.py -k live_pcgamingwiki_source_to_evidence_chain -q`
  - Offline sample command generating `.piko/summaries/real_source_pilot_2_chain_sample.json`
- Results:
  - `python -m pytest`: 55 passed, 2 skipped in 0.74s. Both skipped tests are explicit live connector smoke tests, so ordinary pytest remains offline.
  - `python -m packages.workflows.article_pipeline`: completed; default `real_collection_performed=False`; `verification_report.status=pass`; `publish_decision=verified_candidate`.
  - Live source-to-evidence smoke: 1 passed, 3 deselected in 0.28s.
  - Offline sample: source_count=1; evidence_count=1; publish_decision=needs_more_evidence; verification_status=pass.
- Failures:
  - none

## Direction Check
- Player need: tested with `Where is the save file location?`.
- Source evidence: PCGamingWiki/MediaWiki normalized source records now flow into evidence cards.
- Structured judgment: source records, evidence cards, verification report, and publish decision remain Pydantic/JSON-serializable.
- Clear guide output: no player-facing answer is generated from insufficient source candidates.
- Traceable sources: evidence card `source_id` is checked against workflow source records.
- Risk warnings: candidate evidence carries a risk note and publish stays blocked until answer-level evidence exists.

## Prohibited Items Check
- Real external API: allowed only in explicit double opt-in live smoke.
- Real crawler: not added.
- HTML page full-text scraping: not added.
- Long raw source storage: not added.
- Reddit / Steam / Google / ProtonDB: not connected.
- Real publishing: not added.
- Deployment: not added.
- Admin review / human approval: not added.
- Unsourced claims: no player-facing claim or ranked solution is created from candidate-only evidence.

## Risks And Notes
- Unfinished: page-level MediaWiki content extraction for save-file-location evidence is not implemented.
- Risks: PCGamingWiki search snippets can contain wiki template markup; they are safe for candidate evidence but not ready for player-facing prose.
- Assumptions: candidate evidence should pass traceability verification while still blocking publishing through gates and `needs_more_evidence`.

## Next Recommendation
- Suggested next round: Piko-verify for real-source-pilot-2.
- Why: confirm real source records enter evidence chain under explicit opt-in, ordinary tests stay offline, traceability failures are caught, and insufficient evidence blocks publish-ready outcomes.
