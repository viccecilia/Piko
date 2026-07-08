# Round ID: REV-4-R03

Round Name: Real Discovery API And Window Results

本轮目标:

把 REV-4 的热门游戏和热门问题结果展示在 API 与本地可视化窗口中，让操作员能看到“当前热游、棘手问题、已有答案/未解决/冲突/高风险”的排行。

本轮任务:
- 执行任务:
  - 扩展 `/discovery/rankings` 或新增 real discovery preview endpoint，返回 hot games、hot questions、question buckets、source trace、mode、real_collection_performed。
  - 扩展 `/discovery/funnel-window` 或 `/discovery/window`，显示中文结果：当前最热游戏、棘手问题、已有答案、未解决高热、冲突答案、高风险阻断。
  - 如果没有真实 endpoint，页面必须显示“当前为 fixture/mock-live preview，不代表全网实时结果”。
- 测试任务:
  - API probe 返回 hot games 和 question buckets。
  - Window HTML 包含上述中文栏目。
  - 默认请求不触网。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-4-R03.md`。
  - 生成 stage summary `.piko/summaries/worker_REV-4.md`。

允许修改:

- `apps/api/routes/discovery.py`
- `packages/discovery/*`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`
- `.piko/summaries/worker_REV-4-R03.md`
- `.piko/summaries/worker_REV-4.md`
- `.piko/round_status.json`

禁止修改:

- 不要发布、部署或进入文章生成。
- 不要默认触网。
- 不要保存 raw/full source。
- 不要绕过 verification 或放宽 Gate。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- API/window probe

完成定义:

- REV-4 三个 round summary 和 stage summary 都存在。
- 操作员能在窗口看到热游和问题排行。
- 输出清楚区分 fixture/mock-live/real-source。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
