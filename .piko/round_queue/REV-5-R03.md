# Round ID: REV-5-R03

Round Name: Candidate Artifact And Funnel Report

本轮目标:

生成一个完整的真实/模拟真实漏斗报告 artifact，回答：当前最热游戏是什么、这些游戏有什么棘手问题、找到了哪些解决方案线索、哪个 topic 被选为文章候选。

本轮任务:
- 执行任务:
  - 写入 `artifacts/discovery_reports/latest_real_market_funnel_report.json`。
  - 报告包含 hot games、hard problems、solution signals、candidate selection、blocked/watchlist reasons、mode、source trace、安全字段。
  - 报告必须可被 `/discovery/funnel-window` 或 API 读取/展示。
  - 报告必须明确 `publish_ready=false`、`publishing_performed=false`。
- 测试任务:
  - artifact exists 且 JSON 可解析。
  - artifact 不包含 raw_text/body/selftext/content/full_comments/raw_page_text/authorization/api_key/secrets。
  - API 或 CLI 能读取 latest report。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-5-R03.md`。
  - 生成 stage summary `.piko/summaries/worker_REV-5.md`。

允许修改:

- `packages/discovery/*`
- `apps/api/routes/discovery.py`
- `artifacts/discovery_reports/*`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`
- `.piko/summaries/worker_REV-5-R03.md`
- `.piko/summaries/worker_REV-5.md`
- `.piko/round_status.json`

禁止修改:

- 不要发布、部署、commit、push。
- 不要保存 raw/full source。
- 不要把 candidate artifact 标成 publish approval。
- 不要绕过 verification 或放宽 Gate。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- artifact JSON parse probe

完成定义:

- REV-5 三个 round summary 和 stage summary 都存在。
- 最新漏斗报告可回答热游、问题、方案线索、候选选择。
- 报告安全字段正确。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
