# Round ID: SOURCE-PROVIDER-3-R02

Round Name: Provider Status Artifact

本轮目标:

生成 provider status artifact，明确当前是 validated_external_url 还是 deploy_ready_pending_host。

本轮任务:
- 执行任务:
  - 汇总 strategy、package、external URL validation。
  - 输出 provider_status、external_provider_validated、approved_url、blocked_reason、next_action。
  - approved_url 如含 query secret 必须 redacted。
- 测试任务:
  - 测试状态字段一致。
  - 测试 URL secret redaction。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SOURCE-PROVIDER-3-R02.md` 和 `.piko/summaries/worker_SOURCE-PROVIDER-3.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/source_provider/*`
- `.piko/summaries/worker_SOURCE-PROVIDER-3-R02.md`
- `.piko/summaries/worker_SOURCE-PROVIDER-3.md`
- `.piko/round_status.json`

禁止修改:

- 不保存敏感 URL 参数。

必须运行的验证:

- Provider status tests

完成定义:

- operator 能看懂外部 provider 当前状态。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
