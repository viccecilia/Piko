# Round ID: ENDPOINT-4-R01

Round Name: REAL Funnel Success Handoff

本轮目标:

把成功 normalized live signals 交给 REAL funnel，生成 local approved endpoint 范围内的 Top candidates 和 pain buckets。

本轮任务:
- 执行任务:
  - 生成 REAL success handoff artifact。
  - 包含 Top 5/Top 20 candidate preview、pain buckets、selected safe candidate。
  - 明确 source_scope=local_approved_endpoint。
- 测试任务:
  - 测试 Top candidates 来自 live success artifact。
  - 测试 watchlist/high-risk 不进入 publish candidate。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_ENDPOINT-4-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/real_data_pilot/*`
- `artifacts/discovery_reports/*`
- `artifacts/local_endpoint/*`
- `.piko/summaries/worker_ENDPOINT-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不声称全网实时 Top 5。

必须运行的验证:

- REAL success handoff tests

完成定义:

- REAL 漏斗成功路径跑通，但范围被正确限定。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
