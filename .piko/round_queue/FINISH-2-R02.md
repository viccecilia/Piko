# Round ID: FINISH-2-R02
Round Name: Topic Funnel Ranking From Real Signals

本轮目标:

对真实信号执行漏斗式筛选：热门主体、热门问题、已解决可写、未解决监控、高风险阻断、冲突答案解释。

本轮任务:
- 执行任务:
  - 生成 Top items、need clusters、answered/watchlist/conflict/high-risk/must-check buckets。
  - 保留 score components、source trace、evidence readiness。
  - 输出 `latest_real_signal_funnel.json` 的 ranking section。
- 测试任务:
  - 测试 answered 高热问题可进入 content candidate。
  - 测试 unanswered 进入 watchlist。
  - 测试 high-risk blocked。
  - 测试 conflict 不作为直接发布许可。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_FINISH-2-R02.md` 和 `.piko/summaries/worker_FINISH-2.md`。

允许修改:

- `packages/final_mvp/**`
- `packages/discovery/**`
- `tests/**`
- `artifacts/final_mvp/**`

禁止修改:

- 不得把 ranking 结果当 publish approval。
- 不得丢失 source trace。
- 不得保存完整帖子正文。

必须运行的验证:

- FINISH funnel ranking 专项测试
- `python -m pytest tests\test_discovery_search.py -q`

完成定义:

- 漏斗分类完整。
- 可写候选、监控候选、阻断候选边界清楚。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

