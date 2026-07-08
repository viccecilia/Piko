# Round ID: STORY-1-R02

Round Name: Coverage History And Dedup

本轮目标:

维护内容覆盖历史，避免每天重复讲同一个 skill，除非有明确的新版本、新角度或新案例。

本轮任务:
- 执行任务:
  - 创建或更新 `artifacts/storytelling/coverage_history.json`。
  - 记录 topic_id、title、covered_at、source_refs、template_version、reuse_allowed_reason。
  - 对 latest candidate 做 dedup 检查。
  - 如果重复且没有新角度，选择备用候选或标记 `needs_operator_choice=true`。
- 测试任务:
  - 验证 history JSON 可解析。
  - 验证重复候选不会无理由进入内容生成。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_STORY-1-R02.md`。
  - 生成 `.piko/summaries/worker_STORY-1.md`。

允许修改:

- `artifacts/storytelling/*`
- `.piko/summaries/worker_STORY-1-R02.md`
- `.piko/summaries/worker_STORY-1.md`
- `.piko/round_status.json`

禁止修改:

- 不要删除历史记录来规避重复检查。
- 不要发布或上传内容。

必须运行的验证:

- Coverage history JSON parse probe。

完成定义:

- 今日候选通过去重，或明确需要人工选择备用主题。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
