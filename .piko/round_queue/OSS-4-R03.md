# Round ID: OSS-4-R03

Round Name: Proposal To CAP And STORY Queue Bridge

本轮目标:

把 OSS 发现的升级提案变成可交给 CAP/STORY 的任务候选，而不是自动改代码。

本轮任务:
- 执行任务:
  - 生成 `artifacts/oss_research/latest_cap_queue_candidates.json`。
  - 生成 `artifacts/oss_research/latest_story_queue_candidates.json`。
  - CAP candidates 必须包含 capability_change_type、risk、tests_needed、verification_needed。
  - STORY candidates 必须包含 topic、hook、why_now、source_refs、template_version_hint。
  - 明确所有 candidates 都是 proposal，不是自动任务执行许可。
- 测试任务:
  - 验证两个 JSON 可解析。
  - 验证 candidates 不会自动创建/执行 round。
  - 验证 STORY candidates 能被 STORY-1 消费。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-4-R03.md`。
  - 生成 `.piko/summaries/worker_OSS-4.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/oss_research/*`
- `.piko/summaries/worker_OSS-4-R03.md`
- `.piko/summaries/worker_OSS-4.md`
- `.piko/round_status.json`

禁止修改:

- 不要自动生成可执行 patch。
- 不要自动执行 CAP/STORY。
- 不要发布内容。

必须运行的验证:

- CAP/STORY candidate JSON parse probes。
- No auto-execute guardrail scan。

完成定义:

- OSS 研究结果可以安全交给 CAP 和 STORY。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
