# Round ID: GROW-5-R01

Round Name: Growth Loop Documentation And Operator Guide

本轮目标:

补全文档，说明每日 GitHub 扫描如何进入 CAP review、如何生成任务草稿、如何由人类确认。

本轮任务:
- 执行任务:
  - 更新或新增 docs，说明 Piko v0.2 growth loop：
    - piko-github 扫描
    - GROW intake/normalization
    - CAP review
    - worker/verify draft package
    - operator approval
    - 后续正式 round queue
  - 明确 `piko-skill` 是对外内容线，不等于 Piko 吸收。
  - 明确所有 generated tasks 都是 draft-only。
- 测试任务:
  - 文档 probe：包含 piko-github、CAP Review、draft-only、human approval、piko-skill separation。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_GROW-5-R01.md`。

允许修改:

- `docs/*`
- `artifacts/growth_loop/*`
- `.piko/summaries/worker_GROW-5-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要声称 Piko 已完全自动吸收能力。
- 不要声称自动发布内容。

必须运行的验证:

- Docs keyword probe。

完成定义:

- 操作员能理解 Piko 成长线和对外内容线的区别。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
