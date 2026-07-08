# Round ID: SKILL-3-R02

Round Name: Eval Runner And Report

本轮目标:

实现 eval runner dry-run 和 report artifact，让 verify 能看到每个 case 的结果。

本轮任务:
- 执行任务:
  - 实现 eval runner。
  - 输出 eval report：total、passed、failed、case_results、blocked_reasons。
  - 将报告接入 skill lifecycle 的 evaluated 状态。
- 测试任务:
  - 测试 pass/fail 统计。
  - 测试失败 eval 不会批准 skill。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-3-R02.md` 和 `.piko/summaries/worker_SKILL-3.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/declarative_eval/*`
- `artifacts/skill_runtime/*`
- `.piko/summaries/worker_SKILL-3-R02.md`
- `.piko/summaries/worker_SKILL-3.md`
- `.piko/round_status.json`

禁止修改:

- 不自动批准失败 skill。

必须运行的验证:

- Eval runner tests

完成定义:

- Eval report 可用于 verify 和 skill lifecycle。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
