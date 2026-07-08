# Worker Summary: real-source-pilot-2-content-benchmark

## Scope
- Completed RSP2-1 through RSP2-4.
- Topic: Stardew Valley save file location and first checks if saves do not appear.

## Source Chain
- Real source: PCGamingWiki / MediaWiki API.
- Query/page: `Stardew Valley`.
- Target section: `Save game data location`.
- Source record: `pcgamingwiki_31535`.
- Evidence cards generated: 4.
- Long raw text saved: no.

## Artifacts
- Source sample: `.piko/summaries/real_source_pilot_2_content_source_sample.json`
- Article JSON: `artifacts/article_drafts/stardew-valley-save-file-location.json`
- Article Markdown: `artifacts/article_drafts/stardew-valley-save-file-location.md`
- Comparison JSON: `artifacts/comparisons/stardew-valley-save-file-location_comparison.json`
- Comparison Markdown: `artifacts/comparisons/stardew-valley-save-file-location_comparison.md`

## Piko Draft
- Direct answer and platform save locations.
- Backup-first troubleshooting.
- Risk warnings against deleting saves, unknown tools, DLLs, and unsafe patches.
- Evidence-to-claim trace.
- Marked `draft_benchmark_only` and `publish_ready=false`.

## Comparison
- Compared against PCGamingWiki, Stardew Valley Wiki Saves, and a Steam Community thread.
- Piko is more concise and risk-filtered.
- Piko still needs another source-verification round before publishing eligibility.

## Verification
- `python -m pytest`: 67 passed, 2 skipped.
- `python -m packages.workflows.article_pipeline`: completed; real_collection_performed=False; verification_status=pass; publish_decision=verified_candidate; publishing_performed=False.

## Prohibited Items Check
- No crawler.
- No full-page raw text storage.
- No copied maps/images/tables.
- No Reddit/Steam/Google/ProtonDB connector.
- No publishing.
- No deploy.
- No git commit.
- No Admin Review backend.

## Remaining Risks
- PCGamingWiki section evidence should be cross-checked against another source before publication.
- Stardew Valley Wiki material was used for comparison notes, not claim extraction.
- The draft is a benchmark artifact, not a public guide.

## Piko-verify Recommendations
- Check generated artifacts for source trace and no long raw text.
- Confirm ordinary pytest skips live tests.
- Confirm article artifact remains `publish_ready=false`.
- Confirm workflow default behavior is unchanged.
