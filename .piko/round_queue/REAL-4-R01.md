# Round ID: REAL-4-R01

Round Name: Source-Backed Article Package

本轮目标:

为 selected safe topic 生成 source-backed internal article package。它不是发布，不是最终文章，只是进入人工确认前的候选包。

本轮任务:
- 执行任务:
  - 从 selected topic、source signals、evidence/ranking trace 生成 article package。
  - 包含 title、brief、outline、key claims、source_ids、evidence_trace、uncertainty、verification_required=true。
  - 设置 publish_ready=false、publishing_performed=false。
- 测试任务:
  - 测试 package source/evidence trace 完整。
  - 测试没有 raw/full source。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REAL-4-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/article_drafts/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_REAL-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不调用发布接口。
- 不生成 publish approval。

必须运行的验证:

- Article package safety tests

完成定义:

- 文章候选包可追溯，可交人工看，不会自动发布。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
