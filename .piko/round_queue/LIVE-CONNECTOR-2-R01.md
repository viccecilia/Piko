# Round ID: LIVE-CONNECTOR-2-R01

Round Name: Endpoint Readiness And Opt-In Check

本轮目标:

检查双 opt-in 和 approved endpoint URL。缺失时必须 blocked_for_endpoint。

本轮任务:
- 执行任务:
  - 检查 `PIKO_ENABLE_DISCOVERY_REAL_SOURCE`、`PIKO_LIVE_DISCOVERY_TEST`、`PIKO_APPROVED_ENDPOINT_URL`。
  - 生成 endpoint readiness artifact。
  - 缺失时写明 missing_config。
- 测试任务:
  - 测试缺配置 -> blocked_for_endpoint。
  - 测试不泄露 endpoint query secret。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-CONNECTOR-2-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/live_connector_pilot/*`
- `.piko/summaries/worker_LIVE-CONNECTOR-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不触网，除非 readiness 完整。

必须运行的验证:

- Endpoint readiness tests

完成定义:

- 系统明确知道能不能 live probe。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
