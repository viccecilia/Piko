# Round ID: SOURCE-PROVIDER-2-R03

Round Name: Provider Package Safety And Versioning

本轮目标:

给静态 endpoint package 增加版本、校验 hash、更新时间和安全摘要。

本轮任务:
- 执行任务:
  - 生成 package manifest。
  - 字段包含 package_version、payload_hash、generated_at、contract_version、safety_flags。
  - 明确 raw_body_saved=false、secrets_retained=false。
- 测试任务:
  - 测试 hash 与 payload 匹配。
  - 测试 safety flags。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SOURCE-PROVIDER-2-R03.md` 和 `.piko/summaries/worker_SOURCE-PROVIDER-2.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/source_provider/*`
- `.piko/summaries/worker_SOURCE-PROVIDER-2-R03.md`
- `.piko/summaries/worker_SOURCE-PROVIDER-2.md`
- `.piko/round_status.json`

禁止修改:

- 不写入 secrets。

必须运行的验证:

- Package versioning tests

完成定义:

- 待部署包可审计、可校验。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
