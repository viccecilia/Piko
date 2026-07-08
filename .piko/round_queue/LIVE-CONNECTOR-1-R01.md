# Round ID: LIVE-CONNECTOR-1-R01

Round Name: Select Approved JSON Endpoint Connector

本轮目标:

从 connector registry 中选择最低风险 live connector：approved_json_endpoint。不得选择 Steam/Reddit/JP/KR/SERP live connector。

本轮任务:
- 执行任务:
  - 读取 connector registry artifacts。
  - 生成 live connector selection artifact。
  - 明确 selected_connector_id=approved_json_endpoint，selection_reason，excluded_connectors。
- 测试任务:
  - 测试 selected connector 是 approved_json_endpoint。
  - 测试 excluded live connectors 未启用。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-CONNECTOR-1-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/live_connector_pilot/*`
- `.piko/summaries/worker_LIVE-CONNECTOR-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不启用其他 live connector。

必须运行的验证:

- Live connector selection tests

完成定义:

- V1 live connector 只选择 approved_json_endpoint。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
