# Round ID: REALDATA-4-R01
Round Name: Realdata Funnel Ranking

本轮目标:

把 provider collection + freshness + dedup cluster 输入 Piko 漏斗，产出真实数据驱动的热门排行和问题桶。

本轮任务:
- 执行任务:
  - 生成 `artifacts/realdata/latest_realdata_funnel.json`。
  - 排出 Top games、answered candidates、watchlist、conflict、high-risk blocked、must-check。
  - 分数包含 heat、freshness、source diversity、answer maturity、risk、Piko value add。
- 测试任务:
  - 测试 answered high-heat 可进入 candidate。
  - 测试 unanswered high-heat 进入 watchlist。
  - 测试 high-risk blocked。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-4-R01.md`。

允许修改:

- `packages/realdata/**`
- `packages/discovery/**`
- `tests/**`
- `artifacts/realdata/**`

禁止修改:

- 不得把 ranking 当 publish approval。
- 不得声明 broad internet coverage。

必须运行的验证:

- REALDATA funnel 专项测试
- `python -m pytest tests\test_discovery_search.py -q`

完成定义:

- 漏斗输出能回答：哪些游戏热、哪些问题棘手、哪些有答案、哪些要监控。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

