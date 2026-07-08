# Round ID: SOURCE-PROVIDER-3-R01

Round Name: External URL Validation Probe

本轮目标:

如果 operator 提供了外部 URL，则验证它；如果没有，则输出 deploy_ready_pending_host。

本轮任务:
- 执行任务:
  - 检查 `PIKO_EXTERNAL_APPROVED_ENDPOINT_URL` 或 `PIKO_APPROVED_ENDPOINT_URL`。
  - 拒绝 localhost/file/fixture。
  - 有外部 URL 时执行 bounded fetch + contract validation。
  - 无 URL 时生成 deploy_ready_pending_host artifact。
- 测试任务:
  - 测试 no URL -> deploy_ready_pending_host。
  - 测试 localhost -> rejected_not_external。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SOURCE-PROVIDER-3-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/source_provider/*`
- `.piko/summaries/worker_SOURCE-PROVIDER-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不把 local URL 算成功。

必须运行的验证:

- External URL validation tests

完成定义:

- 有外部 URL 则验证；没有则清楚待部署。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
