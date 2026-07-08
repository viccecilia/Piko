# Agent Contracts

Each Piko agent is a small role with a stable input and output contract. Agents should receive compact IDs and structured summaries, not full raw documents unless a controlled retrieval step explicitly allows it.

## Shared Input

```json
{
  "game_id": "game_mock_001",
  "game_name": "Example Game",
  "topic": "crash on startup",
  "payload": {}
}
```

## Shared Output

```json
{
  "agent": "keyword_agent",
  "output": {},
  "source_ids": [],
  "mock": true,
  "created_at": "2026-06-21T00:00:00Z"
}
```

## Business Agents

### Keyword Agent

Generates candidate keywords for a game and topic.

Output includes:

- `keywords`

### Pain Agent

Identifies the actual player pain behind a keyword.

Output includes:

- `pain_type`
- `pain_score`
- `blocking_level`
- `search_value`
- `article_candidate`
- `reason`

### Source Agent

Selects source types and source IDs for the player need.

Output includes:

- `sources`
- `real_collection_performed`

Stage 1 must always return `real_collection_performed: false`.

### Evidence Agent

Extracts mock evidence cards and claim candidates.

Output includes:

- `evidence_cards`
- `claim_candidates`

### Conflict Agent

Finds platform mismatch, version mismatch, outdated claims, and risky recommendations.

Output includes:

- `conflicts`
- `warnings`
- `requires_human_review`

### Ranking Agent

Ranks solution candidates by confidence, risk, source strength, and usefulness.

Output includes:

- `ranked_solutions`

### Writer Agent

Drafts from `ArticleBrief` only.

Rules:

- Do not invent facts.
- Do not claim personal testing.
- Do not read full raw sources directly.
- Do not publish.

### Editor Agent

Removes filler and keeps the page direct, sourced, and player-first.

Output includes:

- `style_pass`
- `removed_patterns`
- `editor_note`

## Quality Agent

### Fact-check Agent

Placeholder for checking claim IDs, source IDs, source freshness, platform match, and version match.

