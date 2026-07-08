# Piko Stages, Rounds, And Tasks

This document is the coordination contract for Piko-worker and Piko-verify.
Piko-worker implements one round at a time, in the recommended order below.
Piko-verify validates the same round before the next round starts. The current
plan is continuous implementation with automated result verification; human
review/admin workflow is intentionally skipped for now.

## Worker Prompt

```text
你是 Piko-worker，工作目录是 C:\PycharmProjects\Piko。

请按照 docs/stages_and_rounds.md 的 Recommended Execution Order 连续执行。
每次只执行一个 Round；完成后停止并输出结果，等待 Piko-verify 验证通过后再进入下一轮。

工作原则：
- 严格遵守该 Round 的“允许修改”和“禁止修改”。
- 不接真实外部 API，除非该 Round 明确允许。
- 不生成真实发布内容，除非该 Round 明确允许。
- 暂时跳过人工审核/Admin Review；不要实现 review queue、人工审批后台或人工编辑系统。
- 每个 Round 完成后必须产生可由 Piko-verify 复查的结果证据。
- 所有 agent、gate、workflow 输出必须是结构化 JSON 或 Pydantic model 可序列化结果。
- 代码修改后必须运行该 Round 的“必须运行的验证”。
- 如果发现上游骨架缺口，可以做最小必要修复，但必须在输出中说明。

输出格式必须包含：
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
```

## Verify Prompt

```text
你是 Piko-verify，工作目录是 C:\PycharmProjects\Piko。

请验证 Piko-worker 刚完成的指定 Round。

验证原则：
- 先读取 docs/stages_and_rounds.md 中对应 Round 的目标、任务、允许修改、禁止修改、完成定义。
- 不扩大需求，不替 worker 做大范围重构。
- 优先运行该 Round 的“必须运行的验证”。
- 检查是否有真实外部 API 调用、真实爬虫、真实发布行为、无来源结论、越权修改。
- 检查是否误做了人工审核/Admin Review 相关功能；当前阶段禁止引入 review queue、人工审批后台或人工编辑系统。
- 检查结果是否偏离 Piko 方向：玩家需求、多来源证据、结构化判断、清楚解决路径、来源追溯、风险提示。
- 如发现问题，给出文件路径、具体行为、影响、建议修复方式。

输出格式必须包含：
- 验证结论：通过 / 不通过 / 有条件通过
- 已运行验证
- 发现的问题
- 禁止项检查
- 协作验收结果
- 建议返工任务
```

## Continuous Result Verification Rule

Every round must leave behind verifiable evidence:

- Passing command output or summarized failures.
- Updated tests for the behavior added in that round.
- A sample JSON output when agents, gates, workflow, source extraction, or publishing eligibility changed.
- A durable worker summary file under `.piko/summaries/`.
- A durable verify summary file under `.piko/summaries/` after verification.
- A direction check proving the result still supports Piko's core path:

```text
player need -> source evidence -> structured judgment -> clear guide output -> traceable sources -> risk warnings
```

No round may advance if Piko-verify marks it `不通过`.

## Worker And Verify Handoff Protocol

Piko-worker and Piko-verify coordinate through the shared file:

```text
.piko/round_status.json
```

This file is the handoff signal. Do not rely on memory from another window.

Detailed summaries live in:

```text
.piko/summaries/
```

The status file should stay compact. Long explanations, changed-file lists,
test evidence, sample JSON, risks, and verification notes belong in summary
files.

Summary file naming:

```text
worker_<ROUND_ID>.md
verify_<ROUND_ID>.md
worker_<STAGE_ID>.md
verify_<STAGE_ID>.md
```

Examples:

```text
.piko/summaries/worker_S1-R01.md
.piko/summaries/verify_S1-R01.md
.piko/summaries/worker_S1.md
.piko/summaries/verify_S1.md
```

### Status Values

`worker_status`:

- `not_started`
- `in_progress`
- `ready_for_verify`
- `needs_fix`
- `complete`

`verification_status`:

- `not_started`
- `in_progress`
- `passed`
- `failed`
- `conditional`

### Worker Rules

Before starting a round, Piko-worker must:

- Read `.piko/round_status.json`.
- Read `docs/stages_and_rounds.md`.
- Start only the `next_round`.
- Set `worker_status` to `in_progress`.
- Set `verification_status` to `not_started`.

After finishing a round, Piko-worker must:

- Create or update `.piko/summaries/worker_<ROUND_ID>.md`.
- Set `current_round` to the round it just finished.
- Set `worker_status` to `ready_for_verify`.
- Set `verification_status` to `not_started`.
- Set `worker_summary` to a short summary of changed files, tests, and risks.
- Set `worker_summary_file` to the worker summary path.
- Keep `next_round` unchanged until Piko-verify passes the round.
- Stop and wait. Do not continue to the next round automatically.

### Verify Rules

Before verifying, Piko-verify must:

- Read `.piko/round_status.json`.
- Verify only when `worker_status` is `ready_for_verify`.
- Read the path in `worker_summary_file`.
- Read the matching round in `docs/stages_and_rounds.md`.

After verification:

- If passed:
  - Create or update `.piko/summaries/verify_<ROUND_ID>.md`.
  - Set `verification_status` to `passed`.
  - Set `last_verified_round` to the verified round.
  - Set `last_completed_round` to the verified round.
  - Set `next_round` to the next item in Recommended Execution Order.
  - Set `worker_status` to `complete`.
  - Set `verification_summary_file` to the verify summary path.
- If failed:
  - Create or update `.piko/summaries/verify_<ROUND_ID>.md`.
  - Set `verification_status` to `failed`.
  - Set `worker_status` to `needs_fix`.
  - Keep `next_round` equal to the failed round.
  - Put required fixes in `verification_summary`.
  - Set `verification_summary_file` to the verify summary path.
- If conditional:
  - Create or update `.piko/summaries/verify_<ROUND_ID>.md`.
  - Set `verification_status` to `conditional`.
  - Set `worker_status` to `needs_fix`.
  - Keep `next_round` equal to the current round unless the condition is documentation-only.
  - Set `verification_summary_file` to the verify summary path.

### Worker Summary Template

Each worker summary must use this shape:

```text
# Worker Summary: <ROUND_ID>

## Round
- Round ID:
- Round Name:
- Stage:
- Started from next_round:

## Scope
- Allowed files touched:
- Files intentionally not touched:
- Upstream fixes made:

## Changes
- Modified files:
- Added files:
- Deleted files:
- Behavioral changes:

## Task Status
- 执行任务:
- 测试任务:
- 协作验收任务:

## Verification Run By Worker
- Commands run:
- Results:
- Failures:

## Sample Output
```json
{}
```

## Direction Check
- Player need:
- Source evidence:
- Structured judgment:
- Clear guide output:
- Traceable sources:
- Risk warnings:

## Prohibited Items Check
- Real external API:
- Real crawler:
- Real publishing:
- Admin review / human approval:
- Unsourced claims:

## Risks And Notes
- Unfinished:
- Risks:
- Assumptions:

## Next Recommendation
- Suggested next round:
- Why:
```

### Verify Summary Template

Each verify summary must use this shape:

```text
# Verify Summary: <ROUND_ID>

## Verdict
- Result: passed / failed / conditional
- Round verified:
- Worker summary file:

## Checks Run
- Commands:
- Results:

## Round Requirements
- Execution tasks:
- Test tasks:
- Collaboration acceptance tasks:
- Completion definition:

## Findings
- Blocking issues:
- Non-blocking issues:
- Evidence:

## Prohibited Items Check
- Real external API:
- Real crawler:
- Real publishing:
- Admin review / human approval:
- Unsourced claims:
- Out-of-scope files:

## Direction Check
- Player need:
- Source evidence:
- Structured judgment:
- Clear guide output:
- Traceable sources:
- Risk warnings:

## Status File Update
- worker_status:
- verification_status:
- last_verified_round:
- next_round:

## Required Fixes
- If failed or conditional, list exact fixes.
```

### User Relay Phrase

After Piko-verify passes a round, the user can tell Piko-worker:

```text
Piko-verify 已通过。请读取 .piko/round_status.json，并继续 next_round。
```

If Piko-verify fails a round, the user can tell Piko-worker:

```text
Piko-verify 未通过。请读取 .piko/round_status.json 的 verification_summary，修复当前 round，不要进入下一轮。
```

This keeps the work continuous while preserving a strict verification gate.

## Stage 0: Project Skeleton And Scope

Goal: establish a runnable project skeleton and lock Piko's first-phase boundaries.

Exit:
- Local API starts.
- `/health` returns ok.
- Agent Registry lists 8 business placeholder agents.
- Tool Registry lists mock tools.
- Workflow runs from start to end.
- Gate modules accept a mock article brief.
- PostgreSQL model draft exists.
- No external API key is required.
- No real publishing behavior exists.

### Round ID: S0-R01

Round Name: Scope And Repository Baseline

本轮目标:
Clarify Piko's product scope, repo layout, and first-stage no-go boundaries.

本轮任务:
- 执行任务:
  - Ensure `README.md` explains Piko as a source-based game guide and player need aggregation platform.
  - Ensure first-stage exclusions are explicit: no real external API, no crawler, no real article generation, no publishing.
  - Ensure `docs/architecture.md`, `docs/source_policy.md`, and `docs/publishing_policy.md` exist.
- 测试任务:
  - Run repository file listing with `rg --files`.
  - Confirm required docs are present.
- 协作验收任务:
  - Worker reports whether current repo matches the Stage 0 scope.
  - Verify confirms no source file introduces real external API behavior.

允许修改:
- `README.md`
- `docs/architecture.md`
- `docs/source_policy.md`
- `docs/publishing_policy.md`
- `docs/stages_and_rounds.md`

禁止修改:
- Do not modify runtime code.
- Do not add external service credentials.
- Do not add real crawling or publishing code.

必须运行的验证:
- `rg --files`
- `python -m pytest`

完成定义:
- Project scope and no-go boundaries are documented.
- Tests pass or failures are clearly unrelated and documented.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S0-R02

Round Name: API And Health Baseline

本轮目标:
Make the FastAPI app reliably start and expose health and registry endpoints.

本轮任务:
- 执行任务:
  - Confirm `apps/api/main.py` creates the FastAPI app.
  - Confirm `/health` returns service status and app name.
  - Confirm API routes for agents, tools, gates, and workflow are registered.
- 测试任务:
  - Add or update tests for `/health`.
  - Add or update tests for route availability.
- 协作验收任务:
  - Worker reports exact endpoints confirmed.
  - Verify runs API tests and checks route registration.

允许修改:
- `apps/api/main.py`
- `apps/api/routes/*`
- `tests/*`

禁止修改:
- Do not introduce authentication.
- Do not introduce database startup requirements.
- Do not call external services.

必须运行的验证:
- `python -m pytest`

完成定义:
- API app imports cleanly.
- `/health` passes test.
- Registered routes are test-covered.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S0-R03

Round Name: Placeholder Agents And Gates

本轮目标:
Ensure all first-stage agents and gates return stable structured outputs.

本轮任务:
- 执行任务:
  - Confirm 8 business agents exist: keyword, pain, source, evidence, conflict, ranking, writer, editor.
  - Keep factcheck as a separate placeholder quality agent.
  - Confirm each agent has a stable name, version, description, and JSON output.
  - Confirm gates return pass/fail with reasons.
- 测试任务:
  - Test agent registry list.
  - Test each gate with a mock article brief.
- 协作验收任务:
  - Worker reports the registered agent count and gate names.
  - Verify checks no agent pretends to use real external data.

允许修改:
- `packages/agents/*`
- `packages/gates/*`
- `packages/shared/schemas.py`
- `tests/*`

禁止修改:
- Do not replace placeholders with model calls.
- Do not add OpenAI, Steam, Reddit, Google, or ProtonDB calls.
- Do not generate real guide content.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Agent Registry lists the 8 business agents.
- Gates are callable and return structured decisions.
- Workflow still runs.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

## Stage 1: Observable Multi-Agent Pipeline

Goal: turn the skeleton into a traceable multi-agent pipeline using mock data.

Exit:
- Unified pipeline state exists.
- Each agent run records input summary, output, status, duration, and errors.
- Article workflow returns a complete run report.
- Gate results aggregate into a publish decision.
- API can trigger one article workflow run.

### Round ID: S1-R01

Round Name: Pipeline State Contract

本轮目标:
Define the shared state object that every agent, gate, and workflow node uses.

本轮任务:
- 执行任务:
  - Add or refine `PipelineState`, `AgentRunRecord`, `GateRunRecord`, and `WorkflowRunReport` schemas.
  - Include fields for player question, game, intent, sources, evidence cards, conflicts, ranked steps, draft, gate results, and decision.
  - Ensure all models serialize cleanly to JSON.
- 测试任务:
  - Add schema serialization tests.
  - Add tests for minimal valid pipeline state.
- 协作验收任务:
  - Worker provides a sample JSON state in the report.
  - Verify validates the sample through tests or direct import.

允许修改:
- `packages/shared/schemas.py`
- `packages/workflows/article_pipeline.py`
- `tests/*`
- Docs only if needed to reflect schema names.

禁止修改:
- Do not add real source collection.
- Do not add model provider calls.
- Do not change public route names unless tests and docs are updated.

必须运行的验证:
- `python -m pytest`

完成定义:
- A single shared pipeline state contract is available and tested.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S1-R02

Round Name: Agent Run Observability

本轮目标:
Make every placeholder agent execution observable and debuggable.

本轮任务:
- 执行任务:
  - Wrap agent execution so each run records agent id, version, input summary, output, status, started/ended timestamps or duration, and error.
  - Keep outputs deterministic for tests.
  - Preserve the existing Agent Registry contract.
- 测试任务:
  - Test successful agent run records.
  - Test a controlled failing agent or failure path if practical.
- 协作验收任务:
  - Worker reports one example agent run record.
  - Verify confirms run records are included in workflow output.

允许修改:
- `packages/agents/*`
- `packages/workflows/article_pipeline.py`
- `packages/shared/schemas.py`
- `tests/*`

禁止修改:
- Do not log secrets.
- Do not use wall-clock-only assertions that make tests flaky.
- Do not add external dependencies unless necessary and documented.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Workflow output contains agent run records for all executed agents.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S1-R03

Round Name: Workflow Run API

本轮目标:
Expose the article pipeline through a stable API endpoint.

本轮任务:
- 执行任务:
  - Add or confirm `POST /workflow/article/run`.
  - Request accepts game and player question.
  - Response returns full workflow run report.
  - Keep mock-only behavior.
- 测试任务:
  - Add API tests for successful run.
  - Add validation test for missing question.
- 协作验收任务:
  - Worker reports request and response examples.
  - Verify calls the endpoint through tests.

允许修改:
- `apps/api/routes/workflow.py`
- `packages/workflows/article_pipeline.py`
- `packages/shared/schemas.py`
- `tests/*`

禁止修改:
- Do not persist runs to database in this round.
- Do not add auth, UI, or external integrations.

必须运行的验证:
- `python -m pytest`

完成定义:
- API can trigger one complete mock workflow and return structured JSON.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S1-R04

Round Name: Publish Decision Aggregation

本轮目标:
Aggregate gate decisions into one clear workflow-level publish decision.

本轮任务:
- 执行任务:
  - Implement publish decision values such as `do_not_publish`, `needs_more_evidence`, `verification_failed`, and `verified_candidate`.
  - Decision must consider failed gates, risk level, evidence sufficiency, and unresolved conflicts.
  - Include recommended next action.
- 测试任务:
  - Test pass, fail, and needs-more-evidence scenarios.
  - Test that risky or uncited content cannot be `verified_candidate`.
- 协作验收任务:
  - Worker reports decision matrix.
  - Verify checks at least one blocked scenario.

允许修改:
- `packages/gates/*`
- `packages/workflows/article_pipeline.py`
- `packages/shared/schemas.py`
- `tests/*`

禁止修改:
- Do not implement real publishing.
- Do not mark mock content publish-ready unless evidence and gates justify it.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Workflow report always includes a defensible publish decision.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

## Stage 2: Local Source Fixtures And Evidence Extraction

Goal: use local sample sources to train the source-to-evidence flow before any real integrations.

Exit:
- Local fixtures represent official, wiki, community, and compatibility sources.
- Source Agent can select candidate local fixtures.
- Evidence Agent extracts evidence cards.
- Conflict Agent detects simple contradictions.
- Fact-check Agent maps draft claims to evidence cards.

### Round ID: S2-R01

Round Name: Local Source Fixture Format

本轮目标:
Create a controlled local source dataset for development and testing.

本轮任务:
- 执行任务:
  - Add `fixtures/sources/` with small markdown or JSON samples.
  - Include source metadata: source id, source type, URL placeholder, title, date, game, trust tier.
  - Include at least one black-screen or launch-issue example.
- 测试任务:
  - Add loader tests for fixture parsing.
  - Validate required metadata fields.
- 协作验收任务:
  - Worker lists fixture files and source types.
  - Verify confirms fixtures are local-only and small.

允许修改:
- `fixtures/sources/*`
- `packages/collectors/*`
- `packages/shared/schemas.py`
- `tests/*`
- Relevant docs.

禁止修改:
- Do not fetch internet content.
- Do not copy long third-party text.
- Do not store raw external articles.

必须运行的验证:
- `python -m pytest`

完成定义:
- Local fixtures can be loaded and validated without network access.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S2-R02

Round Name: Source Candidate Selection

本轮目标:
Make Source Agent select relevant local fixture sources for a player question.

本轮任务:
- 执行任务:
  - Implement deterministic matching over local fixture metadata and content snippets.
  - Return ranked candidate sources with reasons.
  - Preserve the no-network rule.
- 测试任务:
  - Test relevant fixture selection.
  - Test no-match behavior.
- 协作验收任务:
  - Worker reports example question and selected source ids.
  - Verify confirms no network calls exist.

允许修改:
- `packages/agents/source_agent.py`
- `packages/collectors/*`
- `packages/shared/schemas.py`
- `tests/*`

禁止修改:
- Do not add external API clients.
- Do not introduce fuzzy libraries unless justified.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Source Agent selects local source candidates with ranked reasons.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S2-R03

Round Name: Evidence Card Extraction

本轮目标:
Extract structured evidence cards from selected local sources.

本轮任务:
- 执行任务:
  - Implement evidence card schema fields: evidence id, source id, claim, supports, confidence, quote snippet, risk note, observed version.
  - Evidence Agent extracts cards from local fixtures.
  - Keep extraction deterministic and rule-based for now.
- 测试任务:
  - Test evidence extraction from at least two source types.
  - Test evidence cards reference valid source ids.
- 协作验收任务:
  - Worker reports example evidence cards.
  - Verify checks claim-to-source traceability.

允许修改:
- `packages/agents/evidence_agent.py`
- `packages/indexing/evidence_extractor.py`
- `packages/shared/schemas.py`
- `tests/*`

禁止修改:
- Do not summarize unsupported claims.
- Do not produce evidence without a source id.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Workflow report contains evidence cards linked to source ids.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S2-R04

Round Name: Conflict And Fact Trace

本轮目标:
Detect simple evidence conflicts and map draft claims back to evidence.

本轮任务:
- 执行任务:
  - Conflict Agent identifies conflicting evidence by supported action, version, or risk.
  - Fact-check Agent verifies each key draft claim has at least one evidence card.
  - Add unresolved conflicts to workflow report.
- 测试任务:
  - Add fixture with one intentional conflict.
  - Test conflict detection.
  - Test unsupported claim failure.
- 协作验收任务:
  - Worker reports conflict example.
  - Verify confirms unsupported claims are blocked or marked as verification failures.

允许修改:
- `packages/agents/conflict_agent.py`
- `packages/agents/factcheck_agent.py`
- `packages/indexing/claim_trace.py`
- `packages/workflows/article_pipeline.py`
- `tests/*`

禁止修改:
- Do not hide conflicts by dropping evidence.
- Do not let unsupported claims pass silently.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Conflicts and claim traces appear in the workflow report.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

## Stage 3: Editorial Draft Generation

Goal: generate useful, source-backed draft content without AI-flavored filler or false first-hand claims.

Exit:
- Article brief is generated from evidence.
- Draft follows Piko article template.
- Editor pass improves clarity, priority, risk notes, and source language.
- Draft remains unpublished.

### Round ID: S3-R01

Round Name: Article Brief Builder

本轮目标:
Build a structured article brief from player need, evidence, conflicts, and ranked steps.

本轮任务:
- 执行任务:
  - Define article brief schema.
  - Include title, problem statement, recommended first steps, risk notes, source summary, unresolved questions.
  - Build brief in workflow before Writer Agent.
- 测试任务:
  - Test brief generation with sufficient evidence.
  - Test brief marks evidence gaps.
- 协作验收任务:
  - Worker reports sample brief.
  - Verify checks every recommendation is evidence-linked or marked uncertain.

允许修改:
- `packages/workflows/article_pipeline.py`
- `packages/agents/ranking_agent.py`
- `packages/shared/schemas.py`
- `docs/article_template.md`
- `tests/*`

禁止修改:
- Do not create public pages.
- Do not claim first-hand testing.
- Do not invent source details.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Workflow produces a structured article brief before draft generation.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S3-R02

Round Name: Draft Template Output

本轮目标:
Make Writer Agent produce a template-compliant draft from the article brief.

本轮任务:
- 执行任务:
  - Implement draft sections: short answer, steps, risk notes, if-it-fails, sources.
  - Keep draft deterministic and source-backed.
  - Include source ids near claims where appropriate.
- 测试任务:
  - Test required sections exist.
  - Test no unsupported section appears when evidence is missing.
- 协作验收任务:
  - Worker reports one sample draft.
  - Verify checks against `docs/article_template.md`.

允许修改:
- `packages/agents/writer_agent.py`
- `packages/shared/schemas.py`
- `docs/article_template.md`
- `tests/*`

禁止修改:
- Do not add LLM calls yet.
- Do not produce SEO filler.
- Do not publish draft.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Writer output matches the Piko article template and remains draft-only.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S3-R03

Round Name: Editorial Tone And Risk Pass

本轮目标:
Make Editor Agent remove AI-flavored phrasing and enforce player-friendly clarity.

本轮任务:
- 执行任务:
  - Add editorial rules: direct, clear, prioritized, risk-aware, no fake hands-on claims.
  - Editor Agent rewrites draft metadata or sections deterministically.
  - Readability Gate checks banned filler patterns.
- 测试任务:
  - Test banned phrases fail or are rewritten.
  - Test risk notes remain visible.
- 协作验收任务:
  - Worker reports before/after sample.
  - Verify checks no obvious AI-flavored boilerplate remains.

允许修改:
- `packages/agents/editor_agent.py`
- `packages/gates/readability_gate.py`
- `packages/gates/risk_gate.py`
- `docs/article_template.md`
- `tests/*`

禁止修改:
- Do not remove source references to improve tone.
- Do not hide risk warnings.
- Do not add marketing copy.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Edited draft is clearer and passes readability/risk checks when valid.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

## Stage 4: Automated Result Verification

Goal: add strict machine-checkable verification so continuous execution does
not drift away from Piko's mission. This stage replaces the earlier human
review/admin stage for now.

Exit:
- Workflow output can be verified against a result contract.
- Direction checks block outputs that lack player need, source evidence,
  structured judgment, traceability, or risk warnings.
- Verification reports are generated as JSON.
- CI-style tests cover positive and negative examples.
- No admin review queue or human approval system is introduced.

### Round ID: S4-R01

Round Name: Verification Contract

本轮目标:
Define the result verification contract for workflow outputs.

本轮任务:
- 执行任务:
  - Add schemas for `VerificationCheck`, `VerificationReport`, and `VerificationStatus`.
  - Verification must check required fields: player question, game, sources, evidence cards, ranked steps, draft or brief, gate results, publish decision, risk notes, and traceability.
  - Verification status values should include `pass`, `fail`, and `warning`.
- 测试任务:
  - Test valid workflow report passes verification.
  - Test missing evidence fails verification.
  - Test missing risk note warns or fails based on risk level.
- 协作验收任务:
  - Worker reports one passing and one failing verification JSON example.
  - Verify confirms schema is strict enough to catch direction drift.

允许修改:
- `packages/shared/schemas.py`
- `packages/workflows/article_pipeline.py`
- `tests/*`
- `docs/stages_and_rounds.md` only if task wording needs correction.

禁止修改:
- Do not create admin review models.
- Do not create review queue APIs.
- Do not add manual approval as a requirement.
- Do not weaken existing gates.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- A workflow result can be verified by a structured verification contract.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S4-R02

Round Name: Result Verifier Service

本轮目标:
Implement a verifier that checks workflow output after each run.

本轮任务:
- 执行任务:
  - Add a verifier module or service that accepts `WorkflowRunReport`.
  - Checks must cover:
    - one clear player need
    - at least one traceable source when evidence is expected
    - evidence cards linked to source ids
    - ranked steps linked to evidence or marked uncertain
    - unresolved conflicts surfaced
    - risk notes visible for risky actions
    - no real publishing side effect
  - Attach verification report to workflow output or expose it through a helper.
- 测试任务:
  - Test verifier catches unsupported claims.
  - Test verifier catches source id mismatch.
  - Test verifier catches publish-ready decision with failed gates.
- 协作验收任务:
  - Worker reports the verifier checklist and examples.
  - Verify reruns negative tests and confirms failures are meaningful.

允许修改:
- `packages/workflows/*`
- `packages/gates/*`
- `packages/shared/schemas.py`
- `tests/*`

禁止修改:
- Do not rely on manual inspection only.
- Do not remove failed checks from reports.
- Do not make all warnings pass silently.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Every article workflow run can produce or be checked by a verification report.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S4-R03

Round Name: Verification API And Fixtures

本轮目标:
Expose result verification for Piko-verify and future CI checks.

本轮任务:
- 执行任务:
  - Add `POST /workflow/article/verify` or equivalent verification endpoint.
  - Add small local verification fixtures for pass, fail, and warning cases.
  - Ensure endpoint returns structured verification JSON.
- 测试任务:
  - Test verification endpoint with passing fixture.
  - Test verification endpoint with failing fixture.
  - Test endpoint does not trigger publishing or external calls.
- 协作验收任务:
  - Worker reports endpoint payload examples.
  - Verify calls endpoint through tests and checks strict failure behavior.

允许修改:
- `apps/api/routes/workflow.py`
- `packages/workflows/*`
- `packages/shared/schemas.py`
- `fixtures/*`
- `tests/*`

禁止修改:
- Do not add admin UI.
- Do not add human approval endpoints.
- Do not connect external services.

必须运行的验证:
- `python -m pytest`

完成定义:
- Piko-verify can validate workflow results through code and/or API.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

## Stage 5: Real Source Connectors

Goal: add real source connectors gradually after local source governance is stable.

Exit:
- Source connectors are opt-in and rate-limited.
- Raw and cleaned text are stored separately.
- Every item has source id, source type, URL, collection time, and trust metadata.
- No connector is required for local tests.

### Round ID: S5-R01

Round Name: Connector Interface

本轮目标:
Define a connector interface before implementing any real source.

本轮任务:
- 执行任务:
  - Add common connector protocol: search, fetch, normalize, source metadata.
  - Add config flags to disable all real connectors by default.
  - Add mock connector tests.
- 测试任务:
  - Test connector protocol with local fixture connector.
  - Test default config disables network.
- 协作验收任务:
  - Worker reports connector interface.
  - Verify confirms no real network call happens in tests.

允许修改:
- `packages/collectors/*`
- `packages/shared/config.py`
- `packages/shared/schemas.py`
- `tests/*`

禁止修改:
- Do not implement real API calls in this round.
- Do not require API keys.

必须运行的验证:
- `python -m pytest`

完成定义:
- Real connectors can be added later behind a disabled-by-default interface.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S5-R02

Round Name: PCGamingWiki Or MediaWiki Connector

本轮目标:
Add the first real-source connector behind explicit opt-in configuration.

本轮任务:
- 执行任务:
  - Implement one connector only: PCGamingWiki or generic MediaWiki.
  - Respect config flag, timeout, user agent, and minimal result limits.
  - Normalize response into source records.
- 测试任务:
  - Unit test using mocked HTTP responses.
  - Do not require live internet for tests.
- 协作验收任务:
  - Worker reports how to enable connector manually.
  - Verify confirms default tests do not hit network.

允许修改:
- `packages/collectors/pcgamingwiki.py`
- `packages/collectors/mediawiki.py`
- `packages/shared/config.py`
- `packages/shared/schemas.py`
- `tests/*`
- `docs/source_policy.md`

禁止修改:
- Do not add multiple connectors in one round.
- Do not scrape pages without respecting source policy.
- Do not store copied long-form source text in repo.

必须运行的验证:
- `python -m pytest`

完成定义:
- One real connector exists, is opt-in, and has mocked tests.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S5-R03

Round Name: Connector Dedup And Trust Scoring

本轮目标:
Normalize, deduplicate, and score connector results.

本轮任务:
- 执行任务:
  - Implement dedup by URL, canonical title, and content hash where available.
  - Add source trust tiers.
  - Record raw vs cleaned text boundaries.
- 测试任务:
  - Test duplicate inputs collapse correctly.
  - Test trust tiers are assigned by source type.
- 协作验收任务:
  - Worker reports dedup examples.
  - Verify checks source policy is reflected in code.

允许修改:
- `packages/collectors/dedup.py`
- `packages/collectors/*`
- `packages/shared/schemas.py`
- `docs/source_policy.md`
- `tests/*`

禁止修改:
- Do not discard source provenance.
- Do not make community sources equal to official sources by default.

必须运行的验证:
- `python -m pytest`

完成定义:
- Connector results are normalized, deduplicated, and trust-scored.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

## Stage 6: RAG, Indexing, And Memory

Goal: turn collected evidence into reusable retrieval and structured memory assets.

Exit:
- Evidence index exists.
- Retrieval returns source-linked evidence, not raw page dumps.
- Structured memory stores reusable issues, solutions, sources, and article decisions.
- Claim trace links claims to evidence cards.

### Round ID: S6-R01

Round Name: Evidence Index Interface

本轮目标:
Create an index abstraction that can later use LlamaIndex without locking tests to it.

本轮任务:
- 执行任务:
  - Define index builder and retrieval interfaces.
  - Implement local in-memory evidence index.
  - Keep LlamaIndex integration optional.
- 测试任务:
  - Test indexing evidence cards.
  - Test retrieval by question and supported action.
- 协作验收任务:
  - Worker reports retrieval example.
  - Verify confirms retrieval returns evidence ids and source ids.

允许修改:
- `packages/indexing/*`
- `packages/shared/schemas.py`
- `tests/*`

禁止修改:
- Do not pass full raw pages between agents.
- Do not require vector database services.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Workflow can retrieve evidence through an index interface.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S6-R02

Round Name: Structured Memory Store

本轮目标:
Persist reusable judgments in a memory abstraction.

本轮任务:
- 执行任务:
  - Implement memory records for issue, solution, source, and article.
  - Add upsert and lookup methods.
  - Keep in-memory implementation for tests.
- 测试任务:
  - Test memory upsert and lookup.
  - Test workflow can include memory hints.
- 协作验收任务:
  - Worker reports memory record examples.
  - Verify checks memory does not store unbounded raw text.

允许修改:
- `packages/memory/*`
- `packages/workflows/article_pipeline.py`
- `packages/shared/schemas.py`
- `tests/*`

禁止修改:
- Do not introduce Memori as a hard dependency yet.
- Do not store secrets or raw page dumps.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Memory interface stores reusable structured judgments.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S6-R03

Round Name: Version Refresh Signals

本轮目标:
Identify when source changes may require article refresh.

本轮任务:
- 执行任务:
  - Add source freshness fields and article dependency fields.
  - Implement simple refresh signal logic.
  - Mark affected drafts/articles as needs_refresh.
- 测试任务:
  - Test changed source date triggers refresh.
  - Test unchanged source does not trigger refresh.
- 协作验收任务:
  - Worker reports refresh examples.
  - Verify checks refresh is advisory, not auto-publish.

允许修改:
- `packages/memory/*`
- `packages/workflows/source_refresh_pipeline.py`
- `packages/shared/schemas.py`
- `packages/db/models.py`
- `tests/*`

禁止修改:
- Do not auto-update public content.
- Do not schedule background jobs yet unless explicitly requested.

必须运行的验证:
- `python -m pytest`

完成定义:
- System can flag content that should be re-verified after source changes.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

## Stage 7: Public Website And Verified Publishing Candidate

Goal: render only verified, source-backed guide pages with visible provenance.

Exit:
- Public guide page renders.
- Source box is visible.
- Publishing eligibility requires gate pass and result verification pass.
- Sitemap and metadata exist.
- Feedback can be saved for later verification and refresh signals.

### Round ID: S7-R01

Round Name: Public Guide Page Skeleton

本轮目标:
Create the first public guide page template without connecting live publishing.

本轮任务:
- 执行任务:
  - Choose Astro or Next.js based on existing repo direction.
  - Add a guide page template with title, short answer, steps, risk notes, if-it-fails, and sources.
  - Use local mock content only.
- 测试任务:
  - Run frontend build/check if tooling exists.
  - Keep backend tests passing.
- 协作验收任务:
  - Worker reports local preview or build command.
  - Verify checks source box is visible in template.

允许修改:
- `apps/web/*`
- `docs/article_template.md`
- `README.md`
- Frontend config files if needed.

禁止修改:
- Do not connect workflow output to public publishing.
- Do not use copied third-party images or maps.
- Do not create a marketing landing page instead of the guide template.

必须运行的验证:
- `python -m pytest`
- Frontend build/check command if added.

完成定义:
- A public guide template exists with mock source-backed content.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S7-R02

Round Name: Publishing Eligibility Contract

本轮目标:
Define and enforce the contract between verification pass and public publishing eligibility.

本轮任务:
- 执行任务:
  - Add publishing eligibility checks: gate pass, evidence sufficiency, no unresolved high-risk conflicts, and verification pass.
  - Add API or service method that returns eligibility but does not deploy.
  - Document publishing states.
- 测试任务:
  - Test verified valid item is eligible.
  - Test failed gate or failed verification is not eligible.
- 协作验收任务:
  - Worker reports publishing state machine.
  - Verify confirms no automatic deployment occurs.

允许修改:
- `packages/gates/*`
- `packages/workflows/article_pipeline.py`
- `apps/api/routes/*`
- `docs/publishing_policy.md`
- `tests/*`

禁止修改:
- Do not implement real deployment.
- Do not publish unverified drafts.

必须运行的验证:
- `python -m pytest`

完成定义:
- Publishing eligibility is explicit and tested.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S7-R03

Round Name: Feedback Capture

本轮目标:
Capture player feedback for future verification, refresh signals, and memory updates.

本轮任务:
- 执行任务:
  - Add feedback schema: helpful, outdated, did_not_work, missing_info, comment.
  - Add backend endpoint to save feedback to mock repository or database repository.
  - Ensure feedback does not immediately rewrite public content.
- 测试任务:
  - Test feedback endpoint.
  - Test invalid feedback is rejected.
- 协作验收任务:
  - Worker reports feedback payload examples.
  - Verify checks feedback is stored as a verification/refresh signal only.

允许修改:
- `apps/api/routes/*`
- `apps/api/services/*`
- `packages/db/models.py`
- `packages/shared/schemas.py`
- `tests/*`

禁止修改:
- Do not auto-edit articles from feedback.
- Do not collect personal data beyond what is required.

必须运行的验证:
- `python -m pytest`

完成定义:
- Feedback can be captured and queued as a verification/refresh signal.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

## Stage 8: Scale, Operations, And Automation

Goal: scale safely across games, languages, refresh jobs, monitoring, and deployment.

Exit:
- Multi-game jobs work.
- Refresh jobs are observable.
- Token/cost monitoring exists.
- Backups and recovery are documented.
- Agent adapters can be swapped safely.

### Round ID: S8-R01

Round Name: Multi-Game Job Model

本轮目标:
Support running workflows across multiple games without mixing evidence or memory.

本轮任务:
- 执行任务:
  - Add job model for game, locale, question cluster, and run parameters.
  - Ensure game id is included in source, evidence, memory, and article objects.
  - Add safeguards against cross-game evidence leakage.
- 测试任务:
  - Test two-game workflow data stays separated.
  - Test missing game id is rejected.
- 协作验收任务:
  - Worker reports isolation strategy.
  - Verify checks no cross-game source reuse without explicit match.

允许修改:
- `packages/shared/schemas.py`
- `packages/workflows/*`
- `packages/db/models.py`
- `tests/*`

禁止修改:
- Do not add bulk live crawling.
- Do not schedule production jobs.

必须运行的验证:
- `python -m pytest`

完成定义:
- Multi-game workflow state is isolated and tested.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S8-R02

Round Name: Token Cost And Run Monitoring

本轮目标:
Track workflow cost, token estimates, duration, and failures.

本轮任务:
- 执行任务:
  - Extend token monitor for per-agent and per-workflow estimates.
  - Add run summary fields for duration, status, warning count, and error count.
  - Add tests for aggregation.
- 测试任务:
  - Test token/cost aggregation with mock values.
  - Test failed runs report errors.
- 协作验收任务:
  - Worker reports sample monitoring summary.
  - Verify checks monitoring does not log secrets or raw large content.

允许修改:
- `packages/shared/token_monitor.py`
- `packages/workflows/*`
- `packages/agents/*`
- `tests/*`

禁止修改:
- Do not call real model billing APIs.
- Do not store full prompts with secrets.

必须运行的验证:
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`

完成定义:
- Workflow report includes useful monitoring information.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

### Round ID: S8-R03

Round Name: Deployment And Recovery Notes

本轮目标:
Document safe deployment, backups, rollback, and recovery before production use.

本轮任务:
- 执行任务:
  - Add deployment notes for API, DB, worker queue, and web app.
  - Add backup and restore checklist.
  - Add rollback checklist.
  - Keep this as documentation unless deployment target is specified.
- 测试任务:
  - Run existing tests.
  - Check docs links are correct.
- 协作验收任务:
  - Worker reports operational assumptions.
  - Verify confirms no deployment scripts run automatically.

允许修改:
- `docs/operations.md`
- `docs/architecture.md`
- `README.md`

禁止修改:
- Do not deploy anywhere.
- Do not add credentials.
- Do not add destructive scripts.

必须运行的验证:
- `python -m pytest`

完成定义:
- Production-readiness notes exist without performing deployment.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

## Recommended Execution Order

```text
S0-R01 -> S0-R02 -> S0-R03
S1-R01 -> S1-R02 -> S1-R03 -> S1-R04
S2-R01 -> S2-R02 -> S2-R03 -> S2-R04
S3-R01 -> S3-R02 -> S3-R03
S4-R01 -> S4-R02 -> S4-R03
S5-R01 -> S5-R02 -> S5-R03
S6-R01 -> S6-R02 -> S6-R03
S7-R01 -> S7-R02 -> S7-R03
S8-R01 -> S8-R02 -> S8-R03
```

## Current Recommended Next Round

The current recommended next implementation round is:

```text
S1-R01: Pipeline State Contract
```

Reason: Stage 0 skeleton exists. Before adding intelligence or real sources,
Piko needs a stable shared state contract so agents, gates, workflow reports,
API responses, tests, and later persistence all speak the same language.
