# Round ID: ENDPOINT-3-R01

Round Name: Live Connector Success Probe

本轮目标:

使用本地 approved endpoint URL 跑 approved_json_endpoint live connector success path，记录 real_collection_performed=true。

本轮任务:
- 执行任务:
  - 通过 opt-in runner 调用 real endpoint verify/live connector path。
  - 生成 live success artifact。
  - 字段包含 real_collection_performed=true、mode=real-source/local-approved-endpoint、normalized counts。
- 测试任务:
  - 测试 success path。
  - 测试无 opt-in 仍 blocked。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_ENDPOINT-3-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/endpoint_verification/*`
- `artifacts/live_connector_pilot/*`
- `artifacts/local_endpoint/*`
- `.piko/summaries/worker_ENDPOINT-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不调用外部 endpoint。
- 不保存 raw response body。

必须运行的验证:

- Live connector success tests

完成定义:

- 本地 approved endpoint 跑通 live success path。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
