# Round ID: OSS-1-R02

Round Name: High-Star Project Query Rules

本轮目标:

定义每日扫描 GitHub 5000 星以上项目的查询策略和过滤规则，优先发现可用于 Piko 的成熟 agent、skill、workflow、connector、evaluation 项目。

本轮任务:
- 执行任务:
  - 定义 high-star filter：默认 `stars >= 5000`。
  - 定义推荐搜索关键词：agent framework、multi-agent、workflow engine、RAG、evaluation、guardrail、connector、automation、plugin system、content generation、video automation。
  - 定义候选项目字段：stars、recent_activity、license、ecosystem、docs_quality、integration_cost、piko_fit。
  - 如果没有真实 GitHub token 或没有联网许可，输出 fixture/mock research artifact，不伪装真实扫描成功。
- 测试任务:
  - 测试过滤器能排除低星项目。
  - 测试无 token/无 opt-in 时是 fixture mode 或 skipped，而不是失败伪装成功。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-1-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/oss_research/*`
- `.piko/summaries/worker_OSS-1-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要默认联网。
- 不要保存 GitHub token。
- 不要抓取或复制 README 长文。

必须运行的验证:

- High-star filter 测试。
- Fixture/skipped mode 测试。

完成定义:

- 每日 GitHub 扫描策略清晰，可在以后接入真实 GitHub API。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
