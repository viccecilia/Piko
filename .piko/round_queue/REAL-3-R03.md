# Round ID: REAL-3-R03

Round Name: Safe Topic Selection

本轮目标:

从 live pain buckets 选择一个 safe publish_candidate，或在没有安全候选时输出 no_safe_candidate。

本轮任务:
- 执行任务:
  - 运行 topic selector。
  - 输出 selected topic artifact。
  - 字段包含 selected_candidate、selection_reason、evidence_maturity、risk_level、watchlist_excluded、high_risk_excluded。
- 测试任务:
  - 测试只有 safe publish_candidate 可被选择。
  - 测试 no_safe_candidate 不触发 article package。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REAL-3-R03.md` 和 `.piko/summaries/worker_REAL-3.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_REAL-3-R03.md`
- `.piko/summaries/worker_REAL-3.md`
- `.piko/round_status.json`

禁止修改:

- 不选择 high-risk topic。
- 不选择 unanswered watchlist 作为 publish candidate。

必须运行的验证:

- Topic selection tests

完成定义:

- 有安全候选则选择；没有则诚实停住。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
