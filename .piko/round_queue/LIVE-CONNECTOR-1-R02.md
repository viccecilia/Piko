# Round ID: LIVE-CONNECTOR-1-R02

Round Name: Live Connector Approval Artifact

本轮目标:

建立 live connector approval artifact，明确允许 bounded endpoint verification，但不允许 crawler、HTML scrape、发布或其他 connector live。

本轮任务:
- 执行任务:
  - 生成 approval artifact。
  - 字段包含 connector_id、live_probe_allowed、collection_allowed、allowed_endpoint_type=json、max_payload_bytes、timeout_seconds、max_records、production_activation_allowed=false。
  - 明确 forbidden_connectors。
- 测试任务:
  - 测试 production_activation_allowed=false。
  - 测试 non-approved connector live 被拒绝。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-CONNECTOR-1-R02.md` 和 `.piko/summaries/worker_LIVE-CONNECTOR-1.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/live_connector_pilot/*`
- `.piko/summaries/worker_LIVE-CONNECTOR-1-R02.md`
- `.piko/summaries/worker_LIVE-CONNECTOR-1.md`
- `.piko/round_status.json`

禁止修改:

- 不批准生产启用。
- 不批准 broad live connectors。

必须运行的验证:

- Live connector approval tests

完成定义:

- live 试点有机器可读批准边界。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
