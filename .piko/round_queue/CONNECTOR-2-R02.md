# Round ID: CONNECTOR-2-R02

Round Name: Permission Scope And Audit

本轮目标:

定义 connector permission scope 和 audit log contract，所有 connector 调用都能追踪但不泄露敏感内容。

本轮任务:
- 执行任务:
  - 生成 permission/audit artifact。
  - 字段包含 connector_id、domain_id、allowed_operations、denied_operations、timeout_seconds、max_results、audit_event_shape。
  - allowed_operations 默认只允许 dry_run/verify_contract。
- 测试任务:
  - 测试 live_collect 默认不允许。
  - 测试 audit event 不含 raw response/secrets。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-2-R02.md` 和 `.piko/summaries/worker_CONNECTOR-2.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-2-R02.md`
- `.piko/summaries/worker_CONNECTOR-2.md`
- `.piko/round_status.json`

禁止修改:

- 不启用 live_collect。

必须运行的验证:

- Permission/audit tests

完成定义:

- Connector 权限和审计边界清晰。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
