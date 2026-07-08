# Round ID: REV-4-R01

Round Name: Hot Game Ranking From Endpoint Signals

本轮目标:

让 endpoint-fed signals 能产出当前热门游戏 Top 5 / Top 20 排行，并清楚标记来源模式：fixture、mock-live、real-source 或 skipped。

本轮任务:
- 执行任务:
  - 扩展 hot game ranking，使其可消费 endpoint adapter 输出的 `GameHeatSignal`。
  - 排名应综合 Steam rank、review velocity、discussion velocity、update recency、cross-region mentions、source diversity。
  - 输出 Top 5 / Top 20，包含每个游戏的 score inputs 和 reasons。
  - 如果没有 live endpoint，则输出 fixture/mock-live preview，并明确不是实时全网结果。
- 测试任务:
  - mock-live 热游 ranking 可运行。
  - Top 5 排名稳定且包含 score inputs。
  - skipped live 不会伪装成 real-source。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-4-R01.md`。

允许修改:

- `packages/discovery/*`
- `apps/api/routes/discovery.py`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`
- `.piko/summaries/worker_REV-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要默认触网。
- 不要 crawler 或 scrape HTML。
- 不要发布、部署、commit、push。
- 不要默认调用 LLM。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`

完成定义:

- Endpoint-fed hot game ranking 能输出 Top 5 / Top 20。
- mode 和 real_collection_performed 真实可信。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
