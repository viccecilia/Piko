# Round ID: PROVIDER-LIVE-2-R01
Round Name: SERP Provider Package

本轮目标:

生成 SERP snippets provider approved JSON package，作为最小真实 provider 覆盖的优先入口。

本轮任务:
- 执行任务:
  - 生成 `artifacts/provider_live/serp-approved.json`。
  - 包含 search snippet 风格的 hot_games / player_questions 摘要。
  - 保留 snippet，不保存页面正文。
- 测试任务:
  - 测试 SERP package 可被 REALDATA normalizer 消费。
  - 测试 raw/full source 字段不存在。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_PROVIDER-LIVE-2-R01.md`。

允许修改:

- `packages/provider_live/**`
- `tests/**`
- `artifacts/provider_live/**`

禁止修改:

- 不得调用搜索引擎页面 scrape。
- 不得复制完整网页正文。

必须运行的验证:

- SERP provider package 专项测试

完成定义:

- SERP package 可作为 `PIKO_SERP_DISCOVERY_URL` 的 payload 来源。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

