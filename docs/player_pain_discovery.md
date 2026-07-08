# Player Pain Discovery

Piko's discovery layer is a funnel for finding player questions worth turning
into source-backed content.

## Funnel

```text
hot game candidates
-> player question signals
-> need clusters
-> answer status
-> evidence and risk scoring
-> content decision
```

The current implementation is fixture-first and offline by default. It does
not scrape Steam, Reddit, Google, Korean, Japanese, or other communities yet.
Those sources should be added later as opt-in collectors that normalize into
the same question signal contract.

## Decisions

- `publish_candidate`: hot enough, answered, evidence quality is acceptable.
- `watchlist_waiting_for_answer`: hot, but no credible answer exists yet.
- `conflict_explainer`: hot enough, but answers conflict.
- `evergreen_candidate`: stable long-term player need.
- `rising_opportunity`: rapidly growing issue that should be watched early.
- `blocked_high_risk`: unsafe fixes, unknown tools, destructive actions, or security risk.
- `insufficient_evidence`: not enough source quality to write.
- `ignore`: low current value.

## Scoring Contract

Discovery scores are bounded integers from 0 to 100. Output clusters expose
the score inputs in `score_inputs` so operators can see why a candidate landed
in a decision bucket.

| Input | Source field | Meaning |
| --- | --- | --- |
| `game_heat` | `GameHeatSignal.heat_score` | Overall current game demand from rank, review velocity, community post velocity, update recency, and cross-region mentions. |
| `question_heat` | `PlayerNeedCluster.heat_score` | Demand for a player question cluster from game heat, engagement, replies, duplicates, and 24h growth. |
| `answer_status` | `PlayerNeedCluster.answer_status` | Whether credible answers exist: answered, unanswered, conflicting, partial, or unknown. |
| `evidence_quality` | `PlayerNeedCluster.evidence_quality` | Average source/evidence quality for the clustered question signals. |
| `conflict_score` | `PlayerNeedCluster.conflict_score` | Strength of conflicting answers. Any hot conflict should become a synthesis/explainer candidate, not a fake single answer. |
| `risk_level` | `PlayerNeedCluster.risk_level` | Low, medium, or high risk. High risk blocks publishing-style recommendations. |
| `freshness_score` | `PlayerNeedCluster.freshness_score` | Current freshness from recent growth, patch tags, and recent game updates. |
| `evergreen_value` | `PlayerNeedCluster.evergreen_value` | Long-term utility, especially save locations, settings, routes, and cross-language repeated questions. |
| `competition_gap` | `PlayerNeedCluster.competition_gap` | Estimated gap between player need and existing clear answers. High gap can make a sourced evergreen page useful. |
| `actionability_score` | `PlayerNeedCluster.actionability_score` | Whether the topic can become one focused, useful Piko page. |
| `piko_value_add_score` | `PlayerNeedCluster.piko_value_add_score` | Whether Piko can add real value through source traceability, ranking, risk warnings, and clarity. |

Clusters also expose `topic_score_components`, which bundles topic heat,
urgency, evidence maturity, conflict level, risk level, freshness, evergreen
value, competition gap, actionability, and Piko value add into one explainable
object.

## Topic Lifecycle And Actionability

`topic_lifecycle` helps operators distinguish:

- `new`
- `rising`
- `stable`
- `declining`
- `resolved`
- `stale`

Lifecycle never bypasses answer or evidence maturity. A hot unresolved topic can
be `rising`, but it should still go to watchlist or evidence gathering rather
than becoming a publish candidate.

`actionability_label` explains whether a topic can become one useful Piko page:

- `single_page_answerable`
- `needs_more_sources`
- `too_broad`
- `too_risky`
- `too_visual`

Map/image-heavy topics are marked `too_visual` so Piko does not copy maps,
images, or tables. High-risk topics are marked `too_risky` and must not enter
normal article generation.

## Competition Gap And Content Opportunity

`competition_gap` is different from `evidence_quality`:

- `evidence_quality` estimates whether the available source signals are credible enough.
- `competition_gap` estimates whether existing web material appears strong, weak, fragmented, stale, or absent.

The current competition gap is fixture/manual only. Piko does not scrape search
results or copy competitor pages. Clusters expose:

- `competition_gap`
- `competition_gap_status`
- `content_opportunity_score`
- `content_opportunity_reasons`

`content_opportunity_score` combines topic heat, answer state, evidence
maturity, risk, actionability, competition gap, and Piko value add. High-risk
and watchlist topics are penalized so they do not rank as normal content
creation candidates just because they are hot.

Piko value-add reasons should be specific, not marketing filler. Supported
reason types include:

- single-page clarity
- risk ordering
- cross-language bridge
- conflict explanation
- stale or fragmented source refresh
- focused scope
- evidence discipline

Decision priority is intentionally conservative:

| Priority | Rule | Decision |
| --- | --- | --- |
| 1 | `risk_level=high` | `blocked_high_risk` |
| 2 | `answer_status=conflicting` and `question_heat>=55` | `conflict_explainer` |
| 3 | `answer_status=unanswered` and `question_heat>=60` | `watchlist_waiting_for_answer` |
| 4 | `answer_status=answered`, `question_heat>=50`, `evidence_quality>=60`, and `piko_value_add_score>=40` | `publish_candidate` |
| 5 | `growth_score>=70` or `freshness_score>=75`, with `question_heat>=55` | `rising_opportunity` |
| 6 | `evergreen=true` and `evidence_quality>=55` | `evergreen_candidate` |
| 7 | `cross_language=true` or `competition_gap>=65`, with `evidence_quality>=55` | `evergreen_candidate` |
| 8 | `evidence_quality<45` | `insufficient_evidence` |
| 9 | none of the above | `ignore` |

This scoring contract is not publishing permission. It only routes a player
need into the next internal workflow: article drafting, monitoring, conflict
explanation, or evidence gathering.

## Current Entry Points

CLI:

```bash
python -m packages.discovery.search_cli --min-game-heat 50 --limit 5
python -m packages.discovery.search_cli --min-game-heat 50 --limit 5 --view summary
python -m packages.discovery.search_cli --min-game-heat 50 --limit 5 --report
python -m packages.discovery.search_cli --decision publish_candidate --intent save_file --lifecycle resolved --actionability single_page_answerable --min-opportunity 80 --limit 3
```

API:

```text
POST /discovery/search
```

Example request:

```json
{
  "query": "stardew save",
  "game_name": "Stardew Valley",
  "regions": ["en", "jp"],
  "source_types": ["steam_discussion", "wiki_comment"],
  "search_intents": ["save_file"],
  "topic_lifecycles": ["resolved"],
  "actionability_labels": ["single_page_answerable"],
  "min_content_opportunity_score": 80,
  "answer_statuses": ["answered"],
  "decisions": ["publish_candidate"],
  "limit": 5
}
```

The API and CLI filters are search/triage controls only. They do not trigger
article generation, source collection, LLM calls, publishing, or deployment.

Internal view:

```text
GET /discovery/window
```

Report endpoint:

```text
POST /discovery/report
```

## Normalized Hot-Game Sources

Future hot-game collectors should normalize into `GameHeatSignal` instead of
passing source-specific payloads through the funnel.

| Source category | Normalized fields |
| --- | --- |
| Steam charts/reviews | `steam_player_rank`, `steam_review_velocity`, `region_signals` |
| Twitch/YouTube/social video | `community_post_velocity`, `cross_region_mentions` |
| Reddit/Discord/forums | `community_post_velocity`, `region_signals`, `cross_region_mentions` |
| Japanese/Korean communities | `region_signals`, `cross_region_mentions` |
| Patch/DLC/news signals | `update_recency_days`, `community_post_velocity` |

One noisy source should not make every game hot. Game heat blends rank, review
velocity, community velocity, update recency, and cross-region mentions.

## Region Signals And Source Coverage

Topic clusters expose regional signal fields so Piko can see repeated needs
before collapsing everything into one global score:

- `region_signal_summary`
- `region_signal_score`
- `cross_region_repeat`
- `language_gap_opportunity`

Cross-region repeat can add Piko value because a useful page may bridge EN,
JP, and KR communities with clearer source traceability. This is still only a
prioritization signal.

Planned topic source coverage is tracked through `source_coverage`:

| Planned source type | Current status |
| --- | --- |
| `steam_discussion` | fixture only |
| `reddit` | fixture only |
| `discord_forum` | planned gap |
| `official_forum` | fixture only |
| `wiki_comment` | fixture only |
| `jp_community` | planned gap |
| `kr_community` | planned gap |
| `serp_snippet` | fixture only |

`source_coverage` lists current source types, planned source types, missing
source types, regional gaps, coverage ratio, and coverage level. It does not
start collection, crawl Discord/forums, or save raw source content.

## Question Signal Contract

`PlayerQuestionSignal` is source-agnostic and metadata-first:

- required: `question_id`, `game_id`, `game_name`, `question_text`, `source_type`
- useful metadata: `source_region`, `language`, `source_title`, `url`, `created_at`
- scoring fields: engagement, replies, duplicates, 24h growth, accepted/official answer flags, conflict count, evidence quality, competition gap, Piko value add
- safety fields: `risk_level`, tags, short `snippet`, and metadata

Do not store raw full post bodies, copied maps, copied tables, images, login-only
content, paywalled content, credentials, or long snippets. Snippets are bounded
by schema and fixtures stay short.

## Need Keys

The deterministic classifier currently recognizes:

- `save_file_location`
- `save_recovery_risk`
- `crash_after_update`
- `settings_steam_deck`
- `build_loadout`
- `controller_input_issue`
- `map_exploration_route`
- `quest_route`
- `hidden_item`
- `general_player_question`

Each need key maps to a deterministic `search_intent`:

| Need key | Search intent |
| --- | --- |
| `crash_after_update` | `bug_fix` |
| `controller_input_issue` | `bug_fix` |
| `save_file_location` | `save_file` |
| `save_recovery_risk` | `save_file` |
| `settings_steam_deck` | `settings` |
| `build_loadout` | `build` |
| `quest_route` | `quest_blocker` |
| `hidden_item` | `hidden_item` |
| `map_exploration_route` | `map_exploration` |
| `general_player_question` | `walkthrough` |

Cross-language handling is intentionally simple: tags, regions, and repeated
known terms can group repeated questions, while source regions are preserved in
the cluster. This is not translation certainty. A later embeddings or LLM
normalization step can improve multilingual dedup, but it must still keep source
traceability and short snippets.

Clusters expose `normalization_hints` for deterministic EN/JP/KR terms such as
save, location, bug, settings, map, quest, and hidden. These hints are a narrow
classification aid, not a claim of full translation or semantic understanding.
Representative questions are selected from question heat, evidence quality,
language/source readability, and text length, while minority-language examples
remain in `representative_questions` and `source_regions`.

## Watchlist

Hot unanswered clusters become `DiscoveryWatchlistItem` records. These are
fixture/in-memory contracts only, not scheduled jobs.

Watchlist states are explicit:

- `watching`
- `answer_seen`
- `evidence_ready`
- `stale`
- `closed`

Promotion triggers are candidate signals:

- official reply
- accepted answer
- high-upvote answer
- wiki update
- patch notes update
- cross-language answer

Promotion never means publish-ready. It only recommends sending the cluster to
the evidence pipeline.

Refresh planning is also metadata-only. `refresh_interval_hours` and
`next_check_reason` describe when an operator or future opt-in worker should
check again, but Piko does not add Celery/Redis scheduling, background polling,
or real community requests here. High-growth unresolved topics can receive a
shorter suggested interval, while stale topics receive a longer one.

## Cluster To Article Candidate Handoff

`article_candidate_from_cluster` maps a cluster to:

- candidate id
- cluster id
- game id
- game name
- need key
- player question
- article intent
- decision
- answer status
- risk level
- candidate type
- runnable flag
- source search/query hints
- required source types
- source regions
- risk flags
- safety flags
- safety reasons
- safety notes

All handoff candidates keep:

```json
{
  "publish_ready": false,
  "requires_evidence_pipeline": true
}
```

Candidate safety behavior is conservative:

| Discovery decision | Candidate type | Runnable | Notes |
| --- | --- | --- | --- |
| `publish_candidate` | `solution_candidate` | yes | Can be sent to evidence pipeline, but still not publish-ready. |
| `conflict_explainer` | `synthesis_candidate` | yes | Must explain uncertainty and conflicting answers, not pretend there is one normal fix. |
| `watchlist_waiting_for_answer` | `watchlist_only` | no | Wait for an accepted, official, or otherwise credible answer. |
| `blocked_high_risk` | `blocked_safety_note` | no | High-risk advice is blocked from normal guide generation. |
| `insufficient_evidence` | `evidence_gap_candidate` | no | Needs stronger source evidence first. |

Discovery must not auto-run the writer pipeline or mark anything as publishable.

## Handoff To DA

After TD-8, the Topic Discovery Strengthening queue resumes the paused DA work
at `DA-3-R01`. The handoff is intentionally narrow:

- discovery clusters provide prioritization, source-query hints, and safety flags
- runnable `publish_candidate` or `conflict_explainer` candidates can be sent to deeper evidence analysis
- watchlist and high-risk candidates remain blocked from normal article generation
- DA must re-check evidence, source traceability, risk, and verification before any draft is considered useful

This handoff is not publishing approval. It does not trigger collection, article
generation, LLM writing, deployment, or public publishing by itself.

## Real-Source Discovery Pilot Choice

The selected future pilot source is PCGamingWiki/MediaWiki-style wiki metadata
because it can be queried through documented APIs, bounded to metadata/short
snippets, and normalized into source/question records without crawling pages.

Not selected for the first pilot:

- Steam discussions: useful but noisier and often broader than a single answer.
- Reddit: useful but higher moderation/context risk.
- SERP snippets: useful for demand discovery but weak evidence quality.

Real-source discovery remains disabled by default. The current interface is
fixture-backed and requires both:

```powershell
$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE = "true"
$env:PIKO_LIVE_DISCOVERY_TEST = "true"
```

Normal pytest must stay offline. Without both flags, the live-smoke contract
returns a clear skip reason and performs no request.

TD-7 pilot guardrails:

- selected source: `pcgamingwiki_mediawiki`
- source shape: wiki metadata and short snippet only
- live-smoke flags: `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true` and `PIKO_LIVE_DISCOVERY_TEST=true`
- timeout setting: `PIKO_CONNECTOR_TIMEOUT_SECONDS`, default 5 seconds
- result limit: at most 3 records
- retained fields: question id, game id/name, question text, source type/region/title, URL, engagement/reply/duplicate/growth counts, evidence quality, tags, short snippet, and metadata
- prohibited retention: raw full page text, full posts, images, maps, copied tables, credentials, secrets, and long source bodies

The current TD-7 live smoke is still fixture-backed so ordinary verification
can test the contract without network access. A later round may replace the
fixture-backed source with a single documented MediaWiki API request, but it
must keep the same default-offline behavior, result cap, timeout, short-snippet
retention, and candidate-only output.

## Real Market Discovery Contract

Real Market Discovery is a later opt-in layer for current market signals across
Steam, Reddit, JP communities, KR communities, and SERP/search snippets. It is
disabled by default and must normalize source-specific records into Piko
contracts before any ranking or handoff.

Source categories:

| Source | Retained examples | Prohibited examples |
| --- | --- | --- |
| `steam` | game id/name, rank, review/community velocity, source URL, short snippet | raw reviews, full posts, images, credentials |
| `reddit` | game id/name, thread title, engagement, replies, answer maturity, short snippet | `selftext`, full comments, raw bodies, authorization tokens |
| `jp_community` | game/question metadata, language/region, engagement, short snippet | full copied posts, images, maps, raw content |
| `kr_community` | game/question metadata, language/region, engagement, short snippet | full copied posts, raw content, credentials |
| `serp_snippet` | query/title/URL, ranking metadata, short search snippet | full pages, copied tables, scraped page bodies |

Required normalized hot-game fields include game id, game name, source category,
source URL, observed time, rank or velocity, and region. Required normalized
player-question fields include question id, game id/name, question text, source
category, source URL/title, observed time, engagement/reply/duplicate counts,
answer maturity, conflict count, and bounded snippet.

Real-market collection requires both:

```powershell
$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE = "true"
$env:PIKO_LIVE_DISCOVERY_TEST = "true"
```

Endpoint configuration is source-specific:

- `PIKO_STEAM_DISCOVERY_URL`
- `PIKO_REDDIT_DISCOVERY_URL`
- `PIKO_JP_COMMUNITY_DISCOVERY_URL`
- `PIKO_KR_COMMUNITY_DISCOVERY_URL`
- `PIKO_SERP_DISCOVERY_URL`

Limits are bounded by `PIKO_REAL_MARKET_MAX_SOURCES`,
`PIKO_REAL_MARKET_MAX_RECORDS_PER_SOURCE`, `PIKO_CONNECTOR_TIMEOUT_SECONDS`,
and `PIKO_CONNECTOR_USER_AGENT`. Ordinary tests and client paths stay fixture
and offline. Real-market output is candidate signal only, not publishing
permission.

## Real Market Discovery Operator Guide

Fixture mode is the default operator path:

```powershell
python -m packages.discovery.search_cli --min-game-heat 50 --limit 5
```

Fixture mode does not touch the network, does not call LLMs, does not publish,
and reports `real_collection_performed=false`.

Bounded live smoke is optional and skip-first:

```powershell
python -m packages.discovery.real_market_live_smoke --query "Stardew Valley" --limit-per-source 3
```

The live smoke only runs when all of the following are true:

- `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
- `PIKO_LIVE_DISCOVERY_TEST=true`
- at least one approved endpoint is configured, such as `PIKO_STEAM_DISCOVERY_URL`
- the endpoint returns bounded JSON records, not raw pages

If flags or endpoints are missing, the live smoke returns `status=skipped` with
a clear reason. This is expected during normal development and verification.
Do not treat a skipped live smoke as a failed build unless the round explicitly
requires a configured live endpoint.

The live smoke stores only a short verification summary:

- source summaries
- record counts
- at most three sample game records
- at most three sample question records
- short snippets and metadata only

It must not store full live response bodies, full posts, `raw_text`, `body`,
`selftext`, `content`, `full_comments`, `raw_page_text`, images, maps, copied
tables, credentials, authorization headers, API keys, or tokens.

Ranking output is available at:

- API: `/discovery/rankings?limit=5`
- Client: `/discovery/window`

Important ranking sections:

- `real_market_hot_games_top_5`
- `real_market_hot_games_top_20`
- `question_ranking_buckets.hot_answered_questions`
- `question_ranking_buckets.hot_unanswered_watchlist_questions`
- `question_ranking_buckets.conflict_answer_topics`
- `question_ranking_buckets.high_risk_blocked_topics`
- `question_ranking_buckets.must_check_guide_topics`

`publish_candidate` means a topic may be handed to the evidence pipeline as an
internal candidate. It is still not publish-ready. `watchlist_waiting_for_answer`
means the topic is hot but should wait for stronger answer maturity.
`blocked_high_risk` means the topic must not become a normal draft.

The RM-4 candidate pilot uses the highest safe `publish_candidate` or a mocked
real-market equivalent when live endpoints are absent. It writes an internal
draft artifact under `artifacts/candidate_drafts/` with:

- `publish_ready=false`
- `publishing_performed=false`
- `candidate_only=true`
- `verification_report`
- safety fields proving discovery is not publishing permission

Do not claim broad real-market coverage unless approved endpoints were
configured and a bounded live smoke actually ran. In normal local verification,
real source live smoke is skipped by default because endpoints are not
configured.

## Approved Real Endpoint Verification

Real Endpoint Verification is the next safety layer after the Real Market
Discovery batch. It verifies approved JSON endpoint payloads before any live URL
is used by operators.

Approved endpoint root shape:

```json
{
  "source": {
    "source_id": "approved_endpoint_001",
    "source_type": "approved_market_json",
    "source_category": "steam",
    "endpoint_type": "json"
  },
  "generated_at": "2026-06-24T00:00:00Z",
  "metadata": {
    "candidate_only": true
  },
  "games": [],
  "questions": []
}
```

`games` must contain hot-game metadata such as game id/name, source category,
source URL, rank or velocity, update recency, region, and cross-region mention
signals. `questions` must contain question id, game id/name, question text,
source category/title/URL, answer maturity, engagement, reply count, risk,
bounded snippet, and tags.

Approved endpoints must be JSON endpoints. HTML pages, raw body endpoints, RSS
full-text dumps, scraped pages, and unbounded source exports are not approved.

Rejected fields include `raw_text`, `raw_body`, `raw_response_body`, `body`,
`selftext`, `content`, `html`, `page_html`, `full_post`, `full_page`,
`full_comments`, `raw_page_text`, `images`, `maps`, `tables`, credentials,
secrets, authorization headers, API keys, and tokens.

The local fixture mirror lives at:

```text
fixtures/real_endpoint/approved_market_payload.json
```

Verify fixture mode:

```powershell
python -m packages.discovery.real_endpoint_verify --fixture
```

Verify live mode only after explicit opt-in:

```powershell
$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE = "true"
$env:PIKO_LIVE_DISCOVERY_TEST = "true"
$env:PIKO_APPROVED_ENDPOINT_URL = "https://approved-json-endpoint.example/market.json"
python -m packages.discovery.real_endpoint_verify --live
```

Without opt-in or without a URL, live verification returns `status=skipped`.
Fixture verification remains default-offline and is the normal pytest path.

REV live smoke summaries are safe to persist only as bounded verification
artifacts, for example:

```powershell
python -m packages.discovery.real_endpoint_verify --fixture --write-artifact
```

The summary artifact is written to:

```text
artifacts/endpoint_verification/latest_endpoint_verification.json
```

It contains status, mode, source metadata, normalized counts, retained fields,
skip reason, and safety flags. It does not contain raw endpoint response bodies,
secrets, authorization headers, full posts, full pages, full comments, images,
maps, copied tables, or HTML. `mode=real-source` is only allowed when a live URL
actually runs under explicit opt-in; fixture and mock-live probes must keep
`real_collection_performed=false`.

## Retrospective And Improvement Signals

Discovery can produce a non-mutating retrospective report with counts for:

- publish candidates
- watchlist candidates
- high-risk blocked clusters
- weak source clusters

Discovery issues can become safe `ImprovementSignal` records, but they must not
auto-apply patches, write raw text to the ledger, publish, deploy, or bypass
operator review.

## Safety

- Default mode is fixture-only.
- `real_collection_performed=false`.
- No crawler is implemented here.
- No publishing is performed.
- Output is a list of candidate clusters for later evidence/article pipelines.
- Discovery output is not publishing permission.
## REV-3 To REV-6 Operator Flow

REV-3 through REV-6 add a local operator-facing flow on top of the approved endpoint contract. It can show approved source registry state, endpoint-fed hot game rankings, hot player-question buckets, safe candidate selection, source query hints, internal article package status, and publish readiness metadata.

This flow remains fixture/mock-live by default. It is not publication approval, does not deploy, does not crawl, does not call an LLM, and does not save raw or full source material.

## LIVE-1 Approved Endpoint Smoke

LIVE-1 is the first small real endpoint connection round. It remains skipped unless the operator provides all three live settings:

- `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
- `PIKO_LIVE_DISCOVERY_TEST=true`
- `PIKO_APPROVED_ENDPOINT_URL=<approved-json-endpoint>`

Missing settings are not failures. They produce a safe skipped artifact with `real_collection_performed=false`, `publishing_performed=false`, and a clear skipped reason.
