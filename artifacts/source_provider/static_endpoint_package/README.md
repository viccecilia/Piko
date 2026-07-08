# Piko Approved JSON Endpoint Package

This package contains a static JSON payload that conforms to Piko's approved endpoint contract.

Files:

- `approved-market.json`

Suggested hosting options:

- GitHub Raw or Gist raw URL
- Cloudflare Pages static asset
- Vercel or Netlify static asset
- User-owned HTTPS JSON endpoint

Rules:

- Do not host it as HTML.
- Do not add raw source bodies, full posts, full comments, credentials, tokens, cookies, API keys, or authorization headers.
- Do not treat localhost, file, or fixture URLs as external endpoints.
- After hosting, set the resulting non-local HTTPS URL in `PIKO_APPROVED_ENDPOINT_URL` and rerun EXTERNAL-ENDPOINT.
