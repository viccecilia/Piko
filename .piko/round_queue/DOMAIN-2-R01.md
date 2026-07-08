# Round ID: DOMAIN-2-R01

Round Name: Gaming Domain Pack Manifest

本轮目标:

把现有 gaming 能力显式封装为 gaming domain pack，而不是 core 默认身份。

本轮任务:
- 执行任务:
  - 生成 gaming domain pack manifest。
  - 包含 source_types、signals、scoring_profile、content_templates、risk_policy、eval_suite。
  - 标注 relation_to_existing_discovery。
- 测试任务:
  - 测试 gaming manifest 可解析。
  - 测试 gaming domain pack activation_status 不自动变更。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-2-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/domain_plugins/gaming*`
- `.piko/summaries/worker_DOMAIN-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不删除现有 gaming artifacts。

必须运行的验证:

- Gaming manifest tests

完成定义:

- Gaming 是明确 domain pack，不是 Piko core。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
