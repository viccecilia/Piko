# Round ID: FINISH-3-R01
Round Name: Evidence-Backed Draft Handoff

本轮目标:

把最高优先级 safe candidate 转成 article/content pipeline handoff，保留 evidence trace 和 verification requirements。

本轮任务:
- 执行任务:
  - 为 selected candidate 生成 source-backed brief。
  - 建立 source_id -> evidence_card -> ranked_claim -> writer_input 的 trace。
  - 输出 `artifacts/final_mvp/latest_content_package.json` 的 handoff section。
- 测试任务:
  - 测试无 evidence 不生成 publishable draft。
  - 测试 source trace 和 evidence trace 完整。
  - 测试 watchlist/high-risk 不进入 writer handoff。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_FINISH-3-R01.md`。

允许修改:

- `packages/final_mvp/**`
- `packages/workflows/**`
- `packages/discovery/**`
- `tests/**`
- `artifacts/final_mvp/**`

禁止修改:

- 不得绕过 article verification。
- 不得把 unsupported claim 放入通过状态。
- 不得默认调用 LLM。

必须运行的验证:

- FINISH content handoff 专项测试
- `python -m packages.workflows.article_pipeline`

完成定义:

- 内容 handoff 可追溯。
- verification_required=true。
- publish_ready=false。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

