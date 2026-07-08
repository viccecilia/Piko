# Round ID: EXTERNAL-ENDPOINT-1-R02

Round Name: External Endpoint Readiness Check

本轮目标:

检查外部 endpoint URL 和双 opt-in。缺失时必须 blocked_for_external_endpoint。

本轮任务:
- 执行任务:
  - 检查 `PIKO_ENABLE_DISCOVERY_REAL_SOURCE`、`PIKO_LIVE_DISCOVERY_TEST`、`PIKO_APPROVED_ENDPOINT_URL`。
  - 确认 URL 不是 localhost/file/fixture。
  - 生成 external endpoint readiness artifact。
- 测试任务:
  - 测试缺配置 -> blocked_for_external_endpoint。
  - 测试 localhost URL 不被标记为 external success。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-1-R02.md` 和 `.piko/summaries/worker_EXTERNAL-ENDPOINT-1.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/external_endpoint/*`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-1-R02.md`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-1.md`
- `.piko/round_status.json`

禁止修改:

- 不泄露 endpoint query secrets。

必须运行的验证:

- External readiness tests

完成定义:

- 是否可跑外部 endpoint 一目了然。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
