# Round ID: CONNECTOR-1-R03

Round Name: Source Governance Policy

本轮目标:

定义 source governance policy，约束来源类型、保留字段、风险级别、禁止存储内容和验收要求。

本轮任务:
- 执行任务:
  - 生成 source governance policy artifact。
  - 定义 approved endpoint、official API、community summary、search snippet、wiki/source doc 等来源等级。
  - 定义禁止项：crawler、HTML scrape、raw body、full comments、credentials。
- 测试任务:
  - 测试 unsafe source policy 被拒绝。
  - 测试 JSON endpoint 仍需 contract validation。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-1-R03.md` 和 `.piko/summaries/worker_CONNECTOR-1.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-1-R03.md`
- `.piko/summaries/worker_CONNECTOR-1.md`
- `.piko/round_status.json`

禁止修改:

- 不放宽现有 source policy。

必须运行的验证:

- Source governance tests

完成定义:

- Connector 有统一来源治理边界。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
