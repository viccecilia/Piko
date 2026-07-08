# Round ID: SKILL-2-R01

Round Name: Worker Run Trace ID

本轮目标:

为 worker run 建立 trace id，把 stage、round、task、artifact、Gate decision 串起来。

本轮任务:
- 执行任务:
  - 定义 worker trace schema。
  - 生成 trace artifact：run_id、stage_id、round_id、task_status、artifact_ids、gate_decisions。
  - 不记录 secrets、raw prompts、长原文。
- 测试任务:
  - 测试 trace id 稳定生成。
  - 测试 trace artifact 不含敏感字段。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-2-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/trace_correlation/*`
- `.piko/summaries/worker_SKILL-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不记录 secrets/token/cookie。

必须运行的验证:

- Trace schema tests

完成定义:

- 每次 worker run 有可关联 trace。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
