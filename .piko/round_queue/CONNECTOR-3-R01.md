# Round ID: CONNECTOR-3-R01

Round Name: Gaming Connector Pack

本轮目标:

为 gaming domain pack 定义 connector pack，映射现有 Steam/Reddit/SERP/MediaWiki/JP/KR/approved endpoint 能力。

本轮任务:
- 执行任务:
  - 生成 gaming connector pack artifact。
  - 标注每个 connector 的 source_type、status、required_env、approved_operations、retained/prohibited fields。
  - 明确所有 live connector 默认 disabled。
- 测试任务:
  - 测试 gaming connector pack 可解析。
  - 测试缺 env 时 blocked_for_endpoint/disabled。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-3-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不修改现有 gaming collection 默认行为。

必须运行的验证:

- Gaming connector pack tests

完成定义:

- Gaming connector 来源被纳入 registry，而不是散落硬编码。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
