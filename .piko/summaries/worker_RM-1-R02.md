# Worker Summary: RM-1-R02

## Round
- Round ID: RM-1-R02
- Round Name: Opt-In And Rate-Limit Policy
- Stage: RM-1
- Started from explicit RM queue request.

## Scope
- Allowed files touched: `packages/shared/config.py`, `packages/discovery/*`, `docs/*`, `tests/test_discovery_search.py`
- Files intentionally not touched: publishing, deployment, crawler, live connector implementations, LLM defaults, Gates
- Upstream fixes made: none

## Changes
- Modified files:
  - `packages/shared/config.py`
  - `docs/player_pain_discovery.md`
  - `tests/test_discovery_search.py`
- Added files:
  - `packages/discovery/real_market.py`
  - `.piko/summaries/worker_RM-1-R02.md`
- Deleted files: none
- Behavioral changes:
  - Added explicit real-market policy helpers.
  - Real-market collection remains impossible unless both discovery opt-in flags are set and requested source endpoints are configured.
  - Added bounded limits for source count and records per source.

## Task Status
- 执行任务: completed
- 测试任务: completed
- 协作验收任务: ready after RM-1 stage completion

## Verification Run By Worker
- Commands run:
  - `python -m pytest tests\test_discovery_search.py -q`
  - `python -m pytest`
- Results:
  - `54 passed in 2.66s`
  - `134 passed, 3 skipped in 3.15s`
- Failures: none

## Env Flags And Endpoint Names
- Required opt-in flags:
  - `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
  - `PIKO_LIVE_DISCOVERY_TEST=true`
- Endpoint env vars:
  - `PIKO_STEAM_DISCOVERY_URL`
  - `PIKO_REDDIT_DISCOVERY_URL`
  - `PIKO_JP_COMMUNITY_DISCOVERY_URL`
  - `PIKO_KR_COMMUNITY_DISCOVERY_URL`
  - `PIKO_SERP_DISCOVERY_URL`
- Limits / request safety:
  - `PIKO_REAL_MARKET_MAX_SOURCES`, bounded to 1-5
  - `PIKO_REAL_MARKET_MAX_RECORDS_PER_SOURCE`, bounded to 1-20
  - `PIKO_CONNECTOR_TIMEOUT_SECONDS`
  - `PIKO_CONNECTOR_USER_AGENT`

## Sample Output
```json
{
  "enabled": false,
  "required_flags": [
    "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true",
    "PIKO_LIVE_DISCOVERY_TEST=true"
  ],
  "limits": {
    "max_sources": 5,
    "max_records_per_source": 20
  },
  "default_offline": true
}
```

## Direction Check
- Player need: real-market inputs remain discovery candidates.
- Source evidence: endpoints are configuration only; no source is contacted.
- Structured judgment: config validation fails clearly if opt-in or endpoints are missing.
- Clear guide output: no guide or draft generated.
- Traceable sources: endpoint categories are explicit.
- Risk warnings: default test/client paths remain offline and fixture-safe.

## Prohibited Items Check
- Real external API: no
- Real crawler: no
- Real publishing: no
- Admin review / human approval: no
- Unsourced claims: no

## Risks And Notes
- Unfinished: RM-1-R03 still needs normalization schema tests/examples.
- Risks: future RM-2 connectors must call `validate_real_market_collection_config` before any request.
- Assumptions: source endpoint URL variables may point to future internal proxy endpoints, not necessarily public APIs.

## Next Recommendation
- Suggested next round: RM-1-R03
- Why: normalize mock Steam/Reddit/JP/KR/SERP payloads into Piko hot-game and question signals without raw retention.
