# Round ID: SKILL-1-R02

Round Name: Skill Lifecycle And Drill Eval

本轮目标:

建立 skill lifecycle：candidate -> evaluated -> approved -> active -> deprecated，并为每个 skill 绑定 drill eval。

本轮任务:
- 执行任务:
  - 定义 lifecycle policy artifact。
  - 定义 drill eval contract：sample input、expected output、forbidden behavior、pass criteria。
  - 增加一个示例 skill：content_quality_assistant，默认 candidate。
- 测试任务:
  - 测试未通过 eval 不可 active。
  - 测试 deprecated skill 不可路由。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-1-R02.md` 和 `.piko/summaries/worker_SKILL-1.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/skill_runtime/*`
- `.piko/summaries/worker_SKILL-1-R02.md`
- `.piko/summaries/worker_SKILL-1.md`
- `.piko/round_status.json`

禁止修改:

- 不把示例 skill 标记为 active，除非测试和 verify 明确批准。

必须运行的验证:

- Skill lifecycle tests

完成定义:

- Skill 有生命周期和可重复 drill eval，不再只是文档概念。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
