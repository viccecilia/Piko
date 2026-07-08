# Round ID: GROW-2-R02

Round Name: Daily CAP Review Report

本轮目标:

把当天标准化候选转成 CAP review report，让操作员看到每个候选为什么进入/不进入 Piko 成长线。

本轮任务:
- 执行任务:
  - 读取 `latest_normalized_candidates.json` 和 `cap_review_policy.json`。
  - 生成 `artifacts/growth_loop/latest_cap_review_report.json`。
  - 每个 candidate 必须有 `decision`、`decision_reason`、`required_tests`、`human_approval_required`、`risk_notes`、`next_action`。
  - next_action 只能是 `draft_worker_task`、`story_pipeline_only`、`watch`、`reject`、`needs_operator_review`。
- 测试任务:
  - 验证 report JSON 可解析。
  - 验证没有 candidate 自动变成 active。
  - 验证每个非 reject candidate 都有 required_tests。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_GROW-2-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/growth_loop/*`
- `.piko/summaries/worker_GROW-2-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要修改 CAP active registry。
- 不要自动生成可执行 patch。

必须运行的验证:

- CAP review report JSON parse probe。
- Decision safety tests。

完成定义:

- 操作员可以看到每日候选的 CAP 判断和下一步建议。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
