# Round ID: SOURCE-PROVIDER-4-R02

Round Name: Operator Provider Instructions

本轮目标:

给 operator 一份简洁说明：如何把静态包变成外部 URL，如何验证，如何交回 Piko。

本轮任务:
- 执行任务:
  - 生成 operator instructions artifact/markdown。
  - 包含 GitHub Raw/Gist 和静态托管两条路径。
  - 包含验证命令和失败处理。
- 测试任务:
  - 检查文档存在。
  - 检查不包含真实凭据。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SOURCE-PROVIDER-4-R02.md` 和 `.piko/summaries/worker_SOURCE-PROVIDER-4.md`。

允许修改:

- `docs/*`
- `artifacts/source_provider/*`
- `.piko/summaries/worker_SOURCE-PROVIDER-4-R02.md`
- `.piko/summaries/worker_SOURCE-PROVIDER-4.md`
- `.piko/round_status.json`

禁止修改:

- 不要求 operator 暴露敏感凭据。

必须运行的验证:

- Operator instruction presence/safety probe

完成定义:

- 人可以按说明创建外部 approved JSON URL。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
