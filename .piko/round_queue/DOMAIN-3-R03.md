# Round ID: DOMAIN-3-R03

Round Name: AI Tools Content And Eval Pack

本轮目标:

为 ai_tools 生成内容模板和 eval，证明 Piko 不只会写游戏内容。

本轮任务:
- 执行任务:
  - 定义 ai_tools content templates：项目介绍、工具对比、集成风险、选型建议。
  - 生成 ai_tools eval suite。
  - 生成一个 internal content package fixture。
- 测试任务:
  - 测试 content package source trace 完整。
  - 测试 publish_ready=false。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-3-R03.md` 和 `.piko/summaries/worker_DOMAIN-3.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/domain_plugins/*`
- `artifacts/content_quality/*`
- `.piko/summaries/worker_DOMAIN-3-R03.md`
- `.piko/summaries/worker_DOMAIN-3.md`
- `.piko/round_status.json`

禁止修改:

- 不发布内容。

必须运行的验证:

- AI tools content/eval tests

完成定义:

- ai_tools 能生成内部候选内容包并通过 eval。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
