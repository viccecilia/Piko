# Round ID: CONNECTOR-4-R03

Round Name: Connector Eval And Readiness Score

本轮目标:

为每个 connector 生成 readiness score，决定是否可进入未来 live approval round。

本轮任务:
- 执行任务:
  - 生成 connector readiness report。
  - 评分维度：contract_complete、credential_safe、source_policy_safe、domain_bound、tests_present、live_ready。
  - live_ready 默认 false，除非所有条件满足。
- 测试任务:
  - 测试缺 endpoint/credentials 时 live_ready=false。
  - 测试 unsafe policy 评分为 blocked。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-4-R03.md` 和 `.piko/summaries/worker_CONNECTOR-4.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-4-R03.md`
- `.piko/summaries/worker_CONNECTOR-4.md`
- `.piko/round_status.json`

禁止修改:

- 不把 connector 标记为 live_ready，除非证据完整。

必须运行的验证:

- Connector readiness tests

完成定义:

- 每个 connector 的实战准备度清楚可验。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
