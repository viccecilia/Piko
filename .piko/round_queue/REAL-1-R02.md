# Round ID: REAL-1-R02

Round Name: Live Endpoint Contract Verification

本轮目标:

在 readiness 允许时执行 approved endpoint contract verification；如果不允许，则写 blocked artifact 并停止后续真实采集。

本轮任务:
- 执行任务:
  - readiness can_run_live=true 时运行 live endpoint verification。
  - can_run_live=false 时生成 blocked_for_endpoint verification artifact。
  - 验证 endpoint 返回 JSON object，字段符合 approved endpoint contract。
- 测试任务:
  - 测试 invalid endpoint shape -> failed_contract_validation。
  - 测试 blocked artifact real_collection_performed=false。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REAL-1-R02.md` 和 `.piko/summaries/worker_REAL-1.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/endpoint_verification/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_REAL-1-R02.md`
- `.piko/summaries/worker_REAL-1.md`
- `.piko/round_status.json`

禁止修改:

- 不保存 raw response body。
- 不继续处理 invalid contract。

必须运行的验证:

- Endpoint contract verification tests

完成定义:

- endpoint 合同验证通过，或安全 blocked/failed。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
