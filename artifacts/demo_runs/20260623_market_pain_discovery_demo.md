# Piko Market Pain Discovery Demo

Run date: 2026-06-23

Mode: fixture-backed safe demo

Safety state:
- real_collection_performed=false
- publishing_enabled=false
- publish_ready=false for discovery outputs
- no crawler, deploy, publishing, default LLM, or real network collection used

## Commands Run

```powershell
python -m packages.discovery.search_cli --min-game-heat 50 --limit 10 --view summary
python -m packages.discovery.search_cli --decision publish_candidate --limit 10 --view summary
python -m packages.discovery.search_cli --decision watchlist_waiting_for_answer --limit 10 --view summary
python -m packages.discovery.search_cli --min-game-heat 50 --limit 10 --report
Invoke-RestMethod -Uri http://127.0.0.1:8000/discovery/search -Method Post -ContentType 'application/json' -Body '{"min_game_heat":50,"limit":5}'
```

## Funnel Summary

| Decision | Count | Meaning |
| --- | ---: | --- |
| publish_candidate | 1 | Has enough answer/evidence maturity to enter the evidence/article pipeline |
| conflict_explainer | 1 | Has conflicting answers and should become a synthesis/uncertainty brief |
| watchlist_waiting_for_answer | 1 | Hot player pain, but no accepted/official answer yet |
| blocked_high_risk | 1 | Risk is too high for normal guide generation |
| ignore | 1 | Not valuable/actionable enough right now |

## Market Pain Candidates

### 1. Stardew Valley - save file location

- Decision: publish_candidate
- Intent: save_file
- Opportunity score: 87
- Heat score: 53
- Evidence quality: 75
- Actionability: single_page_answerable
- Risk: low
- Why it matters: repeated EN/JP demand, fragmented existing answers, clear one-page value.
- Recommended next action: send_to_evidence_pipeline.

### 2. Hades II - Steam Deck/settings/controller issues

- Decision: conflict_explainer
- Intent: settings
- Opportunity score: 55
- Heat score: 55
- Evidence quality: 56
- Actionability: single_page_answerable
- Risk: low
- Why it matters: players have multiple conflicting fixes; Piko can compare them and explain uncertainty.
- Recommended next action: prepare_conflict_brief.

### 3. Hades II - crash after latest patch

- Decision: watchlist_waiting_for_answer
- Intent: bug_fix
- Opportunity score: 19
- Heat score: 91
- Evidence quality: 28
- Actionability: needs_more_sources
- Risk: medium
- Why it matters: very hot and urgent, but not enough credible answer maturity yet.
- Recommended next action: add_to_watchlist until accepted/official fix appears.

### 4. Stardew Valley - third-party save recovery tool

- Decision: blocked_high_risk
- Intent: save_file
- Opportunity score: 0
- Heat score: 44
- Evidence quality: 20
- Actionability: too_risky
- Risk: high
- Why it matters: players may damage saves or follow unsafe tool advice.
- Recommended next action: block normal publishing; prepare only safety warning framing if needed.

### 5. Hades II - beginner build/loadout

- Decision: ignore
- Intent: build
- Opportunity score: 52
- Heat score: 42
- Evidence quality: 57
- Actionability: too_broad
- Risk: low
- Why it matters: broad build content needs tighter scoping before Piko should spend pipeline resources.
- Recommended next action: no_action for now.

## Recommended Demo Next Step

Use the highest-scoring publish candidate:

`Stardew Valley - save file location`

Then run it through the evidence pipeline and article pipeline as a source-backed draft candidate. Keep the output as draft/review only; do not publish.
