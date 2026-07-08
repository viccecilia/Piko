# Source Policy

Piko is source-based. Core claims must trace back to source IDs.

## Current Default Rule

The default system uses local fixtures and mock/source IDs. It performs no real collection, no scraping, and no external API calls.

Real connector code is opt-in only. `PIKO_ENABLE_REAL_CONNECTORS` defaults to `false`; tests use mocked HTTP responses. Do not enable real connectors until source governance, rate limits, source attribution, and storage boundaries are reviewed.

## PCGamingWiki / MediaWiki Pilots

The controlled real-source pilot is limited to the PCGamingWiki/MediaWiki connector path. It is still disabled by default. Normal tests must use mocked HTTP responses and must not require live internet.

Manual local opt-in for a single live smoke request requires both switches:

```powershell
$env:PIKO_ENABLE_REAL_CONNECTORS = "true"
$env:PIKO_LIVE_CONNECTOR_TEST = "true"
```

Unset these variables or set them to `false` for normal development and CI.

Pilot connector requirements:

- Send the configured Piko user agent.
- Use the configured timeout.
- Clamp search result limits to a small bounded value.
- Return structured source metadata: `source_id`, `source_type`, `url`, `title`, `retrieved_at`, and `trust_tier`.
- Keep snippets/clean text short and do not pass long raw page bodies into workflow output.
- Keep normal HTTP behavior unit-tested with mock responses; the live smoke must be explicitly opted in.
- For Pilot 1, use one source, one query, and result limit no higher than 3.
- For Pilot 2, normalized PCGamingWiki/MediaWiki records may enter the evidence chain only as `source_candidate` evidence until page-level extraction supports the specific player question.
- If source candidates do not support an answer-level claim, mark `needs_more_evidence` and keep publishing blocked.
- Do not expand this pilot to Reddit, Steam, Google, ProtonDB, or broad crawling.

## Allowed Future Source Types

- Official patch notes and support pages
- PCGamingWiki
- ProtonDB
- Steam discussions and reviews
- MediaWiki or wiki.gg pages
- Reddit discussions
- Search result snippets or suggestions

## Source Handling Principles

- Store source metadata and text separately.
- Assign a stable `source_id`.
- Keep `raw_text` for traceability.
- Use `clean_text` for extraction.
- Extract evidence cards before handing information to agents.
- Do not pass full raw pages across every agent.
- Do not copy images, maps, tables, or unique guide formatting.
- Mark platform and version scope.
- Mark source freshness.
- Treat unofficial fixes with caution.
- Keep local fixtures small and purpose-written; do not store copied long-form third-party articles in the repository.
- Connector results must preserve source type, URL, trust tier, raw/clean boundary, and source ID.

## Claim Requirements

Every core solution should include:

- `source_ids`
- platform scope
- confidence
- risk level
- last checked date

## LLM Writer Input Boundary

The optional WriterAgent LLM adapter is a drafting aid only. It must not search for sources, extract evidence, decide final factcheck status, publish, or bypass gates.

Allowed LLM inputs are bounded structured fields only:

- player question
- game
- article intent
- evidence cards
- ranked steps
- source IDs
- short snippets already approved for evidence cards
- risk notes
- uncertainty notes

Blocked LLM inputs:

- `raw_text` or full webpage/source bodies
- credentials, secrets, passwords, API keys, authorization headers, access tokens, refresh tokens
- unbounded copied guide text, tables, images, maps, or scraped HTML

The adapter is disabled by default. Live use requires explicit `PIKO_ENABLE_LLM_WRITER=true`, `PIKO_LIVE_LLM_TEST=true`, and an externally supplied `OPENAI_API_KEY`. If the LLM path fails, Piko must fall back to rule-based writing and keep the artifact unpublished.

## Blocked Or Downgraded Content

Piko should block or downgrade recommendations involving:

- Deleting saves without backup
- Replacing executable files
- Downloading unknown DLLs or patches
- Disabling security protections
- Cheats, exploits, bypasses, or anti-cheat circumvention

## Before Enabling Real Sources

- Confirm the target source allows the intended access pattern.
- Add rate limiting and timeout policy.
- Add user-agent/contact policy.
- Add mocked tests that do not require live internet.
- Confirm no connector is required for default local tests.
- Confirm raw text is not passed between every agent.
