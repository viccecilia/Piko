# Round ID: REALDATA-2-R02
Round Name: Live Provider Collection Artifact

本轮目标:

输出真实 provider collection artifact，明确 full / partial / blocked coverage。

本轮任务:
- 执行任务:
  - 生成 `artifacts/realdata/latest_provider_collection.json`。
  - 汇总 hot_games、player_questions、source_summary、provider_statuses。
  - 设置 `coverage_status` 为 `blocked_for_provider_endpoints` / `partial_real_provider_coverage` / `provider_coverage_ready`。
- 测试任务:
  - 测试没有 endpoint 时 blocked。
  - 测试一个 endpoint 成功时 partial。
  - 测试多 endpoint 成功时 provider_coverage_ready。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-2-R02.md`。

允许修改:

- `packages/realdata/**`
- `tests/**`
- `artifacts/realdata/**`

禁止修改:

- 不得将 partial coverage 写成 broad internet coverage。
- 不得把 single approved endpoint 写成 multi-provider coverage。

必须运行的验证:

- REALDATA collection artifact 专项测试

完成定义:

- collection artifact 结构稳定，可供后续 funnel 使用。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

