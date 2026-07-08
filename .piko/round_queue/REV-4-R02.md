# Round ID: REV-4-R02

Round Name: Hot Player Question Discovery

本轮目标:

在热门游戏中发现玩家正在遇到的棘手问题，并按问题热度、答案状态、风险和可写性进行分类。

本轮任务:
- 执行任务:
  - 将 endpoint-fed `PlayerQuestionSignal` 接入现有 discovery funnel。
  - 输出高热问题 Top 20，以及 buckets：已有答案、未解决高热、冲突答案、高风险阻断、必须查攻略。
  - 保留 source_type、source_region、language、url、short snippet、engagement/reply/growth 等结构化字段。
  - 不保存 full posts/full comments/raw body。
- 测试任务:
  - mock-live questions 能生成 buckets。
  - 高风险问题不会进入 normal draft。
  - unanswered high-heat 问题进入 watchlist。
  - conflict 问题进入 conflict_explainer。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-4-R02.md`。

允许修改:

- `packages/discovery/*`
- `packages/collectors/*`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`
- `.piko/summaries/worker_REV-4-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要默认触网。
- 不要抓完整帖子、完整评论或网页正文。
- 不要自动生成/发布文章。
- 不要调用 translation API。
- 不要绕过 verification 或放宽 Gate。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`

完成定义:

- 热门玩家问题能按漏斗 bucket 输出。
- 每条问题可追溯 source metadata。
- 安全分流正确。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
