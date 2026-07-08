# Piko SOURCE-PROVIDER External Approved JSON Provider Queue

Method: Stage-batch file queue workflow.

Purpose:

SOURCE-PROVIDER prepares a real externally reachable approved JSON endpoint provider for Piko. The goal is to move beyond local endpoint success and safety blocking by creating an externally hosted or deploy-ready approved JSON URL that can later be used by EXTERNAL-ENDPOINT to prove true external live success.

Stage labels:

- SOURCE-PROVIDER-1 Provider Strategy And Contract
- SOURCE-PROVIDER-2 External Static Endpoint Package
- SOURCE-PROVIDER-3 External URL Validation
- SOURCE-PROVIDER-4 External Endpoint Handoff To Piko
- SOURCE-PROVIDER-5 Final Verification And Operator Instructions

Execution order:

```text
SOURCE-PROVIDER-1-R01 -> SOURCE-PROVIDER-1-R02
SOURCE-PROVIDER-2-R01 -> SOURCE-PROVIDER-2-R02 -> SOURCE-PROVIDER-2-R03
SOURCE-PROVIDER-3-R01 -> SOURCE-PROVIDER-3-R02
SOURCE-PROVIDER-4-R01 -> SOURCE-PROVIDER-4-R02
SOURCE-PROVIDER-5-R01 -> SOURCE-PROVIDER-5-R02
```

Provider options:

- GitHub Raw / Gist raw URL
- Cloudflare Pages / Vercel / Netlify static JSON
- Existing user-owned HTTPS API endpoint
- Localhost/file/fixture URLs are not valid external providers

Global guardrails:

- Do not publish to a remote host unless credentials/authorization and operator approval are explicitly available.
- Do not store tokens, cookies, API keys, authorization headers, credentials, or secrets.
- Do not scrape or crawl any website.
- Do not claim external live success unless a non-local HTTP(S) URL is fetched and validated.
- Do not call LLM by default.
- Do not publish articles or social posts.
- Do not bypass verification or relax Gate behavior.

Required final verification:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- SOURCE-PROVIDER专项测试
- Provider artifact JSON parse probes
- External URL validation or deploy-ready blocked status probe
- Guardrail scan
