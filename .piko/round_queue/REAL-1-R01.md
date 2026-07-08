# Round ID: REAL-1-R01

Round Name: Approved Live Endpoint Readiness Check

本轮目标:

检查真实数据所需的 approved endpoint 和双 opt-in 是否存在，生成 readiness artifact。没有 endpoint 时必须安全阻断。

本轮任务:
- 执行任务:
  - 检查 `PIKO_ENABLE_DISCOVERY_REAL_SOURCE`、`PIKO_LIVE_DISCOVERY_TEST`、`PIKO_APPROVED_ENDPOINT_URL` 或 CLI approved URL。
  - 生成 live data readiness artifact。
  - 字段包含 opt_in_enabled、endpoint_present、approved_endpoint_url_present、can_run_live、blocked_reason。
- 测试任务:
  - 测试缺少 env 时 readiness 为 blocked_for_endpoint。
  - 测试 artifact 不保存完整 URL query secret。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REAL-1-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_REAL-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不执行真实采集。
- 不保存 secrets。

必须运行的验证:

- Readiness artifact tests

完成定义:

- 系统明确知道能不能跑真实数据。
- 缺 endpoint 时状态清楚，不伪装。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
