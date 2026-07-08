# Round ID: PROVIDER-LIVE-1-R01
Round Name: Provider Package Contract

本轮目标:

定义 SERP / Reddit / Steam provider approved JSON package 合同，确保能被 REALDATA endpoint-only connector 消费。

本轮任务:
- 执行任务:
  - 生成 `artifacts/provider_live/latest_provider_package_contract.json`。
  - 定义 `hot_games` 与 `player_questions` 字段。
  - 标记 `candidate_only=true`、`raw_text_included=false`、`broad_internet_coverage=false`。
- 测试任务:
  - 测试 package contract 覆盖 SERP / Reddit / Steam。
  - 测试 prohibited fields 不允许出现。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_PROVIDER-LIVE-1-R01.md`。

允许修改:

- `packages/provider_live/**`
- `tests/**`
- `artifacts/provider_live/**`
- `.piko/summaries/**`

禁止修改:

- 不得直接采集真实网站。
- 不得默认联网。
- 不得发布或上传。

必须运行的验证:

- PROVIDER-LIVE contract 专项测试

完成定义:

- provider package 合同清楚且机器可读。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

