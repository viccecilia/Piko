# Round ID: REALDATA-4-R02
Round Name: Realdata Topic Selection Policy

本轮目标:

定义真实数据选题策略：优先做高热且已有可靠答案的问题，未解决问题进监控，高风险阻断。

本轮任务:
- 执行任务:
  - 输出 selected_topic、selection_reason、watchlist_topics、blocked_topics。
  - selected_topic 必须包含 source_trace 和 evidence_readiness。
  - 若无合格 topic，输出 no_candidate_reason。
- 测试任务:
  - 测试 selected_topic 条件。
  - 测试无合格 topic 时不生成内容包。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-4-R02.md` 和 `.piko/summaries/worker_REALDATA-4.md`。

允许修改:

- `packages/realdata/**`
- `tests/**`
- `artifacts/realdata/**`

禁止修改:

- 不得选 high-risk topic 进入普通 draft。
- 不得忽略 evidence_readiness。

必须运行的验证:

- REALDATA topic selection 专项测试

完成定义:

- 选题策略可解释且保守。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

