# Round ID: EXTERNAL-ENDPOINT-3-R02

Round Name: Connector Registry External Feedback

本轮目标:

将外部 endpoint 成功/失败反馈给 connector registry，但不自动生产启用。

本轮任务:
- 执行任务:
  - 生成 external connector feedback artifact。
  - 字段包含 last_external_probe_status、readiness_delta、live_ready_candidate、production_activation_allowed=false。
  - blocked/failed 不提升 readiness。
- 测试任务:
  - 测试 production_activation_allowed=false。
  - 测试 blocked/failed readiness 不提升。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-3-R02.md` 和 `.piko/summaries/worker_EXTERNAL-ENDPOINT-3.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/external_endpoint/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-3-R02.md`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-3.md`
- `.piko/round_status.json`

禁止修改:

- 不自动启用 connector。

必须运行的验证:

- External connector feedback tests

完成定义:

- Registry 记录外部 probe 结果但不越权。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
