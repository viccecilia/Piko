# Round ID: ENDPOINT-1-R01

Round Name: Local Approved Endpoint Contract

本轮目标:

定义本地 approved JSON endpoint contract，复用现有 approved endpoint fixture，但通过 HTTP 端点暴露，供 live connector success path 使用。

本轮任务:
- 执行任务:
  - 生成 local endpoint contract artifact。
  - 确认响应 root shape 符合 approved endpoint contract。
  - 标明 scope=local_approved_endpoint、broad_internet_coverage=false。
- 测试任务:
  - 测试 fixture contract validation。
  - 测试 scope 不夸大。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_ENDPOINT-1-R01.md`。

允许修改:

- `packages/*`
- `apps/*`
- `tests/*`
- `docs/*`
- `artifacts/local_endpoint/*`
- `.piko/summaries/worker_ENDPOINT-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不声明全网覆盖。

必须运行的验证:

- Local endpoint contract tests

完成定义:

- 本地 approved endpoint 合同清楚且可验证。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
