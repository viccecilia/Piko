# Round ID: ENDPOINT-2-R03

Round Name: Local Endpoint Smoke

本轮目标:

执行本地 endpoint smoke，确认 HTTP surface、contract validation、opt-in runner 都可用。

本轮任务:
- 执行任务:
  - 运行 local endpoint smoke。
  - 生成 smoke artifact。
  - 字段包含 endpoint_url、status_code、contract_valid、scope=local_approved_endpoint。
- 测试任务:
  - 测试 smoke artifact 可解析。
  - 测试 no raw response body saved。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_ENDPOINT-2-R03.md` 和 `.piko/summaries/worker_ENDPOINT-2.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/local_endpoint/*`
- `.piko/summaries/worker_ENDPOINT-2-R03.md`
- `.piko/summaries/worker_ENDPOINT-2.md`
- `.piko/round_status.json`

禁止修改:

- 不保存完整响应体。

必须运行的验证:

- Local endpoint smoke tests

完成定义:

- 本地 endpoint 可以作为 approved URL 被验证。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
