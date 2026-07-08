# Round ID: DOMAIN-3-R01

Round Name: AI Tools Domain Pack Manifest

本轮目标:

新增 ai_tools domain pack，作为非游戏领域证明。

本轮任务:
- 执行任务:
  - 生成 ai_tools domain pack manifest。
  - 定义 source_types：github_repo、docs_page、release_note、benchmark_post、community_thread。
  - 定义 need types：tool_selection、integration_risk、pricing_change、workflow_template、security_eval。
- 测试任务:
  - 测试 ai_tools manifest 可解析。
  - 测试 activation_status 默认 candidate。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-3-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/domain_plugins/ai_tools*`
- `.piko/summaries/worker_DOMAIN-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不联网抓 GitHub。
- 不调用 GitHub API。

必须运行的验证:

- AI tools manifest tests

完成定义:

- Piko 有第二个非游戏 domain pack。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
