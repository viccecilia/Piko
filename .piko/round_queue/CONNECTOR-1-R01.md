# Round ID: CONNECTOR-1-R01

Round Name: Connector Registry Contract

本轮目标:

定义 Piko 通用 connector registry contract，让不同 domain 可以注册、发现、评估自己的数据源。

本轮任务:
- 执行任务:
  - 定义 connector registry schema。
  - 字段包含 connector_id、domain_ids、source_type、status、endpoint_type、auth_type、retained_fields、prohibited_fields、rate_limit_policy、timeout_policy、approval_required、dry_run_supported。
  - 生成 registry contract artifact。
- 测试任务:
  - 测试必填字段。
  - 测试 status 默认 candidate/disabled。
  - 测试 approval_required=true。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-1-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不启用真实 connector。
- 不删除现有 connector。

必须运行的验证:

- Connector registry contract tests

完成定义:

- Piko 有通用 connector registry contract。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
