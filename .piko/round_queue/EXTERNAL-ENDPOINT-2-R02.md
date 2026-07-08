# Round ID: EXTERNAL-ENDPOINT-2-R02

Round Name: External Contract Validation

本轮目标:

验证外部 endpoint 返回的 JSON 是否符合 approved endpoint contract。

本轮任务:
- 执行任务:
  - 运行 contract validation。
  - 成功时记录 normalized counts。
  - 失败时输出 failed_contract_validation。
- 测试任务:
  - 测试 invalid shape -> failed_contract_validation。
  - 测试 HTML/raw endpoint 被拒绝。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-2-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/external_endpoint/*`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-2-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不绕过 contract validation。

必须运行的验证:

- External contract validation tests

完成定义:

- 外部 endpoint 合同通过或明确失败。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
