# Round ID: SKILL-2-R02

Round Name: Verify Verdict Correlation

本轮目标:

把 Piko-verify 的 verdict 与 worker trace 关联，形成可复盘的闭环。

本轮任务:
- 执行任务:
  - 定义 verify correlation artifact。
  - 字段包含 run_id、worker_summary_file、verification_summary_file、verdict、failed_rounds、regression_tests、next_action。
  - 生成一个当前批次示例 correlation。
- 测试任务:
  - 测试 verdict 只能是 passed/failed/blocked。
  - 测试 failed verdict 必须有 failed_rounds 或 reason。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-2-R02.md` 和 `.piko/summaries/worker_SKILL-2.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/trace_correlation/*`
- `.piko/summaries/worker_SKILL-2-R02.md`
- `.piko/summaries/worker_SKILL-2.md`
- `.piko/round_status.json`

禁止修改:

- 不修改历史 verify 结论。

必须运行的验证:

- Verify correlation tests

完成定义:

- worker 和 verify 能通过 run_id/artifact 互相追踪。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
