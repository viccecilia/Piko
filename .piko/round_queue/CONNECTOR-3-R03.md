# Round ID: CONNECTOR-3-R03

Round Name: Cross-Domain Connector Routing

本轮目标:

建立 connector routing：按 domain_id 和 source_type 查找可用 connector，unknown 安全失败。

本轮任务:
- 执行任务:
  - 实现或定义 connector routing artifact/API。
  - 支持 gaming、ai_tools。
  - unknown domain/connector 返回 safe_fail。
- 测试任务:
  - 测试 gaming 路由。
  - 测试 ai_tools 路由。
  - 测试 unknown 安全失败。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-3-R03.md` 和 `.piko/summaries/worker_CONNECTOR-3.md`。

允许修改:

- `apps/*`
- `packages/*`
- `tests/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-3-R03.md`
- `.piko/summaries/worker_CONNECTOR-3.md`
- `.piko/round_status.json`

禁止修改:

- 不让 unknown fallback 到 gaming。

必须运行的验证:

- Connector routing tests

完成定义:

- Connector 能跨 domain 路由且安全失败。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
