# LIVE-2 Real Approved Endpoint Verification Queue

Method: Stage-batch file queue workflow.

Purpose:

Run a real approved JSON endpoint smoke and prove `real_collection_performed=true` with bounded live data. LIVE-1 proved safe skipped behavior; LIVE-2 is the first stage that should only pass as real-live if an approved JSON endpoint URL is configured and returns contract-compliant data.

Current prerequisite:

- LIVE-1 verified passed.
- Operator must provide or configure a real approved JSON endpoint URL.

Required live environment:

```powershell
$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE="true"
$env:PIKO_LIVE_DISCOVERY_TEST="true"
$env:PIKO_APPROVED_ENDPOINT_URL="https://<approved-json-endpoint>"
```

Approved endpoint contract:

- Must be HTTP/HTTPS JSON.
- Must not be an HTML page.
- Must follow the approved endpoint contract:
  - `source`
  - `generated_at`
  - `metadata`
  - `games`
  - `questions`
- Must return bounded records that normalize into `GameHeatSignal` and `PlayerQuestionSignal`.
- Must not require Piko to store raw response body, full posts, full pages, full comments, images, maps, copied tables, credentials, API keys, authorization headers, or secrets.

Stage labels:

- LIVE-2 Real Approved Endpoint Smoke

Execution order:

```text
LIVE-2-R01 -> LIVE-2-R02 -> LIVE-2-R03
```

Pass/fail rule:

- If no `PIKO_APPROVED_ENDPOINT_URL` is configured, worker may complete with `worker_status=blocked_for_endpoint`, but must not mark LIVE-2 as real-live passed.
- If endpoint is configured and live response passes, worker may set `ready_for_verify`.
- Verify must only mark LIVE-2 passed as real-live if `real_collection_performed=true`.

Global guardrails:

- Do not crawl websites.
- Do not scrape HTML pages.
- Do not store raw response bodies or full source payloads.
- Keep snippets short and bounded.
- Discovery output is candidate signal only, not publishing permission.
- Do not publish, deploy, commit, push, default-call LLMs, call translation APIs, generate/download images, bypass verification, or relax gates.
