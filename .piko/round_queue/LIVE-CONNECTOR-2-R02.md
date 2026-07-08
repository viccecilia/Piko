# Round ID: LIVE-CONNECTOR-2-R02

Round Name: Bounded Endpoint Verification

本轮目标:

在 readiness 完整时执行 bounded live endpoint verification；缺失则生成 skipped/blocked artifact，不伪装成功。

本轮任务:
- 执行任务:
  - 调用现有 approved endpoint verification path。
  - 成功时写 endpoint verification summary。
  - blocked/skipped 时 real_collection_performed=false。
- 测试任务:
  - 测试 blocked path。
  - 测试 success path artifact 不含 raw response body。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-CONNECTOR-2-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/endpoint_verification/*`
- `artifacts/live_connector_pilot/*`
- `.piko/summaries/worker_LIVE-CONNECTOR-2-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不保存 raw response body。
- 不接受 HTML endpoint。

必须运行的验证:

- Endpoint verification tests

完成定义:

- endpoint live/blocked 状态有证据。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
