# Round ID: LIVE-CONNECTOR-4-R02

Round Name: Candidate-Only Ranking Preview

本轮目标:

如果 handoff 有真实 signals，生成 candidate-only ranking preview；否则保留 blocked preview。

本轮任务:
- 执行任务:
  - 生成 ranking preview artifact。
  - 成功时输出 bounded top candidates。
  - blocked 时输出 empty/blocked preview。
  - publish_ready=false、publishing_performed=false。
- 测试任务:
  - 测试 candidate-only。
  - 测试 blocked 不显示 fixture 冒充 live。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-CONNECTOR-4-R02.md` 和 `.piko/summaries/worker_LIVE-CONNECTOR-4.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/live_connector_pilot/*`
- `artifacts/discovery_reports/*`
- `.piko/summaries/worker_LIVE-CONNECTOR-4-R02.md`
- `.piko/summaries/worker_LIVE-CONNECTOR-4.md`
- `.piko/round_status.json`

禁止修改:

- 不用 fixture 冒充 live。

必须运行的验证:

- Ranking preview tests

完成定义:

- REAL funnel 可看到 live/blocked preview，但仍不发布。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
