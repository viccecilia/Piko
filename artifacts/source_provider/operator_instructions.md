# Source Provider Operator Instructions

1. Review `artifacts/source_provider/static_endpoint_package/approved-market.json`.
2. Host that JSON file on an operator-approved non-local HTTP(S) URL.
3. Do not add credentials, tokens, cookies, API keys, authorization headers, raw source bodies, full posts, or full comments.
4. Validate the hosted URL by setting:

```powershell
$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE = "true"
$env:PIKO_LIVE_DISCOVERY_TEST = "true"
$env:PIKO_APPROVED_ENDPOINT_URL = "<external approved json url>"
python -m packages.source_provider.pipeline --write-artifacts
```

5. If validated, rerun EXTERNAL-ENDPOINT with the same URL.

No upload or deployment was performed by this worker.
