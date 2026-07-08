# Round ID: SOURCE-PROVIDER-1-R02

Round Name: External Provider Approval Contract

本轮目标:

定义外部 provider approval contract，确保只有 operator-approved URL 才能进入 EXTERNAL-ENDPOINT。

本轮任务:
- 执行任务:
  - 生成 provider approval contract artifact。
  - 字段包含 provider_type、external_url_required、operator_approval_required、credential_storage_allowed=false、deployment_allowed=false。
  - 明确 prohibited providers：localhost、file、fixture、raw HTML page。
- 测试任务:
  - 测试 prohibited provider 被拒绝。
  - 测试 credential_storage_allowed=false。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SOURCE-PROVIDER-1-R02.md` 和 `.piko/summaries/worker_SOURCE-PROVIDER-1.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/source_provider/*`
- `.piko/summaries/worker_SOURCE-PROVIDER-1-R02.md`
- `.piko/summaries/worker_SOURCE-PROVIDER-1.md`
- `.piko/round_status.json`

禁止修改:

- 不批准未给出的外部 URL。

必须运行的验证:

- Provider approval tests

完成定义:

- 外部 provider 批准边界可验证。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
