# Round ID: PROVIDER-LIVE-4-R01
Round Name: Steam Provider Package

本轮目标:

生成 Steam provider approved JSON package，只保留热度和讨论摘要，不 scrape Steam 页面。

本轮任务:
- 执行任务:
  - 生成 `artifacts/provider_live/steam-approved.json`。
  - 包含 rank、velocity、community_post_velocity、update_recency_days。
  - 明确 raw discussion body 不保存。
- 测试任务:
  - 测试 Steam package 可 normalize。
  - 测试 raw/full fields 不存在。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_PROVIDER-LIVE-4-R01.md`。

允许修改:

- `packages/provider_live/**`
- `tests/**`
- `artifacts/provider_live/**`

禁止修改:

- 不得 scrape Steam。
- 不得保存完整讨论帖。

必须运行的验证:

- Steam provider package 专项测试

完成定义:

- Steam package 可作为 `PIKO_STEAM_DISCOVERY_URL` 的 payload 来源。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

