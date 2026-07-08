# Round ID: CONNECTOR-2-R01

Round Name: Credential Policy And Redaction

本轮目标:

建立 connector credential policy，确保 Piko 不保存真实凭据，只保存安全的引用/状态。

本轮任务:
- 执行任务:
  - 生成 credential policy artifact。
  - 字段包含 credential_storage_allowed=false、secret_reference_allowed=true、redaction_required=true、rotation_required、audit_required。
  - 定义 forbidden credential keys。
- 测试任务:
  - 测试 token/cookie/api_key/authorization 被拒绝或 redacted。
  - 测试 artifact 不保存真实凭据值。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-2-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不写入真实 credentials。

必须运行的验证:

- Credential guardrail tests

完成定义:

- Connector 凭据边界可验证且默认不保存秘密。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
