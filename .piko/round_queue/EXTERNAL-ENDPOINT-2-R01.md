# Round ID: EXTERNAL-ENDPOINT-2-R01

Round Name: Bounded External HTTP Probe

本轮目标:

在 readiness 完整时，执行 bounded external HTTP probe；缺失时写 blocked artifact。

本轮任务:
- 执行任务:
  - 执行 approved endpoint verification path。
  - 限制 timeout、payload size、result counts。
  - 生成 HTTP probe artifact。
- 测试任务:
  - 测试 blocked path。
  - 测试 success path 不保存 raw response body。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-2-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/external_endpoint/*`
- `artifacts/endpoint_verification/*`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不保存完整响应体。

必须运行的验证:

- External HTTP probe tests

完成定义:

- 外部 endpoint 请求成功或安全 blocked。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
