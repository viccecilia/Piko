# Game Guide Domain

The Game Guide domain is Piko's first implementation.

## Domain Goal

Help players answer one concrete question at a time with source-backed, prioritized, low-risk guidance.

## Domain Inputs

- Game ID and game name
- Player question
- Platform/version scope when available
- Source candidates
- Evidence cards

## Domain Outputs

- Article brief
- Ranked solution steps when evidence is sufficient
- Risk notes
- Source summary
- Evidence gaps
- Publishing eligibility candidate status

## Current Boundaries

- Default workflow uses local fixtures.
- Real PCGamingWiki/MediaWiki usage requires explicit opt-in.
- Candidate-only real source evidence must stay `needs_more_evidence`.
- No guide is published automatically.

