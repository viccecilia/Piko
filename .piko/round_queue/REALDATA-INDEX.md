# Piko REALDATA Multi-Provider Production Data Queue

Current recommended next round: REALDATA-1-R01

## Purpose

REALDATA moves Piko beyond one external approved JSON payload and toward real multi-provider market data. The goal is to connect bounded, operator-approved provider endpoints for Steam, Reddit, SERP snippets, JP community, and KR community, then feed their normalized signals into Piko's pluggable domain funnel and content package pipeline.

This queue must not crawl or scrape public websites directly. Every real source must come through an operator-approved JSON summary endpoint or a future explicitly approved official API adapter. Missing endpoints must produce `blocked_for_provider_endpoints`, not fake real success.

## Stages

- REALDATA-1 Provider Contract And Safety Boundary
- REALDATA-2 Multi-Provider Connector Orchestrator
- REALDATA-3 Freshness Provenance And Dedup
- REALDATA-4 Real Market Funnel And Topic Selection
- REALDATA-5 Real Evidence Handoff And Content Package
- REALDATA-6 Operator Surface And Final Verification

## Execution Order

REALDATA-1-R01 -> REALDATA-1-R02
REALDATA-2-R01 -> REALDATA-2-R02 -> REALDATA-2-R03
REALDATA-3-R01 -> REALDATA-3-R02
REALDATA-4-R01 -> REALDATA-4-R02
REALDATA-5-R01 -> REALDATA-5-R02
REALDATA-6-R01 -> REALDATA-6-R02

## Required Provider Env

- `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
- `PIKO_LIVE_DISCOVERY_TEST=true`
- `PIKO_STEAM_DISCOVERY_URL=<approved JSON endpoint>`
- `PIKO_REDDIT_DISCOVERY_URL=<approved JSON endpoint>`
- `PIKO_SERP_DISCOVERY_URL=<approved JSON endpoint>`
- `PIKO_JP_COMMUNITY_DISCOVERY_URL=<approved JSON endpoint>`
- `PIKO_KR_COMMUNITY_DISCOVERY_URL=<approved JSON endpoint>`

Partial provider coverage is allowed only if clearly labeled `partial_real_provider_coverage`. It must not claim broad internet coverage.

## Hard Boundaries

- No crawler.
- No HTML scrape.
- No raw/full source retention.
- No raw Reddit selftext, Steam full discussion body, full comments, images, maps, copied tables, credentials, cookies, or tokens.
- No default network access.
- No default LLM.
- No publishing, upload, deploy, commit, or push.
- No verification bypass or Gate relaxation.
- No broad internet coverage claim unless multiple approved live providers actually pass and the artifact explicitly lists coverage limits.

## Required Final Artifacts

- `artifacts/realdata/latest_provider_contract.json`
- `artifacts/realdata/latest_provider_collection.json`
- `artifacts/realdata/latest_provider_freshness.json`
- `artifacts/realdata/latest_realdata_funnel.json`
- `artifacts/realdata/latest_realdata_content_package.json`
- `artifacts/realdata/latest_realdata_operator_result.json`
- `artifacts/realdata/latest_realdata_readiness.json`

## Required Final Summary

- `.piko/summaries/worker_REALDATA-1-to-REALDATA-6.md`

