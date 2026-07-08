# Piko PROVIDER-LIVE Real Provider Endpoint Package Queue

Current recommended next round: PROVIDER-LIVE-1-R01

## Purpose

PROVIDER-LIVE prepares real provider-approved JSON endpoints for REALDATA. It bridges from `REALDATA blocked_for_provider_endpoints` to at least `partial_real_provider_coverage` by creating provider-specific approved JSON packages, hosting or validating at least one non-local HTTPS provider endpoint, and handing off env instructions to rerun REALDATA.

This queue must not crawl, scrape HTML, save raw/full source, publish, upload, deploy, or claim full/broad internet coverage. If no external provider endpoint can be hosted or validated, the correct result is `deploy_ready_pending_provider_host` or `blocked_for_provider_endpoint`, not fake provider success.

## Stages

- PROVIDER-LIVE-1 Provider Package Contract
- PROVIDER-LIVE-2 SERP Provider Package And Endpoint
- PROVIDER-LIVE-3 Reddit Provider Package And Endpoint
- PROVIDER-LIVE-4 Steam Provider Package And Endpoint
- PROVIDER-LIVE-5 REALDATA Handoff And Final Verification Prep

## Execution Order

PROVIDER-LIVE-1-R01 -> PROVIDER-LIVE-1-R02
PROVIDER-LIVE-2-R01 -> PROVIDER-LIVE-2-R02
PROVIDER-LIVE-3-R01 -> PROVIDER-LIVE-3-R02
PROVIDER-LIVE-4-R01 -> PROVIDER-LIVE-4-R02
PROVIDER-LIVE-5-R01 -> PROVIDER-LIVE-5-R02

## Required Final Artifacts

- `artifacts/provider_live/latest_provider_package_contract.json`
- `artifacts/provider_live/serp-approved.json`
- `artifacts/provider_live/reddit-approved.json`
- `artifacts/provider_live/steam-approved.json`
- `artifacts/provider_live/latest_provider_endpoint_status.json`
- `artifacts/provider_live/latest_realdata_env_handoff.json`
- `artifacts/provider_live/latest_provider_live_readiness.json`

## Hard Boundaries

- No crawler.
- No HTML scrape.
- No direct Steam/Reddit/SERP scraping.
- No raw response body retention.
- No full posts, full comments, full pages, images, maps, copied tables, credentials, cookies, tokens, or API keys.
- No default network unless explicitly validating a hosted approved JSON endpoint.
- No publishing, upload, deploy, commit, or push.
- No broad internet coverage claim.
- At least one provider success can only be `partial_real_provider_coverage`, not full coverage.

