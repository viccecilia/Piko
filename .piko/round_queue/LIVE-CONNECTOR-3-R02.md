# Round ID: LIVE-CONNECTOR-3-R02

Round Name: Connector Registry Feedback

本轮目标:

把 live/blocked 结果反馈给 connector registry readiness，不自动启用 production。

本轮任务:
- 执行任务:
  - 生成 connector feedback artifact。
  - 字段包含 connector_id、last_probe_status、last_probe_at、readiness_delta、production_activation_allowed=false、next_action。
  - 更新 registry-derived artifact 或 feedback report。
- 测试任务:
  - 测试 production_activation_allowed=false。
  - 测试 failed/blocked 不提高 live_ready。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-CONNECTOR-3-R02.md` 和 `.piko/summaries/worker_LIVE-CONNECTOR-3.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/connector_registry/*`
- `artifacts/live_connector_pilot/*`
- `.piko/summaries/worker_LIVE-CONNECTOR-3-R02.md`
- `.piko/summaries/worker_LIVE-CONNECTOR-3.md`
- `.piko/round_status.json`

禁止修改:

- 不自动启用 connector。

必须运行的验证:

- Connector feedback tests

完成定义:

- registry 能学习 probe 状态，但不越权启用。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
