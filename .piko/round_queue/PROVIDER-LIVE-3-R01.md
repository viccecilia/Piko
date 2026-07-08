# Round ID: PROVIDER-LIVE-3-R01
Round Name: Reddit Provider Package

本轮目标:

生成 Reddit provider approved JSON package，只保留结构化摘要，不保存 selftext 或 full comments。

本轮任务:
- 执行任务:
  - 生成 `artifacts/provider_live/reddit-approved.json`。
  - 包含 discussion velocity、reply count、engagement、snippet。
  - 明确 `selftext_saved=false`、`full_comments_saved=false`。
- 测试任务:
  - 测试 Reddit package 可 normalize。
  - 测试 selftext/body/full_comments 不出现。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_PROVIDER-LIVE-3-R01.md`。

允许修改:

- `packages/provider_live/**`
- `tests/**`
- `artifacts/provider_live/**`

禁止修改:

- 不得调用 Reddit 网页 scrape。
- 不得保存帖子全文或评论全文。

必须运行的验证:

- Reddit provider package 专项测试

完成定义:

- Reddit package 可作为 `PIKO_REDDIT_DISCOVERY_URL` 的 payload 来源。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

