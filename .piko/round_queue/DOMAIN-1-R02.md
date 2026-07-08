# Round ID: DOMAIN-1-R02

Round Name: DomainPlugin v1 Contract

本轮目标:

定义 DomainPlugin v1 contract，使任何领域都能用统一接口接入 Piko。

本轮任务:
- 执行任务:
  - 定义 DomainPlugin v1 schema。
  - 字段至少包含 domain_id、version、source_types、signal_schema、normalizer、scoring_profile、content_templates、risk_policy、distribution_targets、eval_suite。
  - activation_status 默认 candidate。
- 测试任务:
  - 测试必填字段。
  - 测试缺 eval_suite 不可 approved。
  - 测试 activation_status 默认不是 active。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-1-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/domain_plugins/*`
- `.piko/summaries/worker_DOMAIN-1-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不自动激活新 domain。

必须运行的验证:

- DomainPlugin contract tests

完成定义:

- 任意领域可以按统一插件合同接入。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
