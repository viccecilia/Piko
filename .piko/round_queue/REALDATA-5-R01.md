# Round ID: REALDATA-5-R01
Round Name: Real Evidence Handoff

本轮目标:

将真实 provider selected_topic 转入 evidence/article handoff，保留 provider trace 和 claim trace。

本轮任务:
- 执行任务:
  - 生成 source-backed brief。
  - 建立 provider_signal -> need_cluster -> evidence_card -> writer_input trace。
  - 输出 `artifacts/realdata/latest_realdata_content_package.json` 的 handoff section。
- 测试任务:
  - 测试 source_trace/evidence_trace 完整。
  - 测试缺 evidence 不 publish_ready。
  - 测试 article_pipeline 仍 verification pass/draft_review。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-5-R01.md`。

允许修改:

- `packages/realdata/**`
- `packages/workflows/**`
- `tests/**`
- `artifacts/realdata/**`

禁止修改:

- 不得绕过 article verification。
- 不得默认调用 LLM。
- 不得把 provider snippet 扩写成无证据断言。

必须运行的验证:

- REALDATA evidence handoff 专项测试
- `python -m packages.workflows.article_pipeline`

完成定义:

- 真实数据可转为可审核内容 brief。
- 内容仍为 internal candidate。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

