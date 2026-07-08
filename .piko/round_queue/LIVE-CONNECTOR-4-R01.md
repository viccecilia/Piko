# Round ID: LIVE-CONNECTOR-4-R01

Round Name: REAL Funnel Handoff

本轮目标:

将 normalized live signals 交给 REAL funnel handoff；blocked 时保持 handoff blocked。

本轮任务:
- 执行任务:
  - 生成 REAL funnel handoff artifact。
  - 成功时包含 hot_game_candidates、need_clusters、source_trace。
  - blocked 时包含 blocked_reason 和 missing_config。
  - 不生成 publish approval。
- 测试任务:
  - 测试 real_collection_performed 与 handoff 状态一致。
  - 测试 blocked 不进入 ranking/article package。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-CONNECTOR-4-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/live_connector_pilot/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_LIVE-CONNECTOR-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不发布。
- 不伪造 REAL Top 5。

必须运行的验证:

- REAL handoff tests

完成定义:

- live connector 结果可进入 REAL 漏斗，或被安全阻断。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
