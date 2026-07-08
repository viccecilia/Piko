# Round ID: CONNECTOR-3-R02

Round Name: AI Tools Connector Pack

本轮目标:

为 ai_tools domain pack 定义 connector pack，覆盖 GitHub repo、release note、docs page、community thread、approved endpoint 等来源。

本轮任务:
- 执行任务:
  - 生成 ai_tools connector pack artifact。
  - 所有 connector 默认 candidate/disabled/dry-run。
  - 定义 source-specific prohibited fields，尤其是 raw repository body、tokens、private repo content。
- 测试任务:
  - 测试 ai_tools connector pack 可解析。
  - 测试不调用 GitHub API、不联网。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-3-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-3-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不真实查询 GitHub。
- 不保存 repo 源码。

必须运行的验证:

- AI tools connector pack tests

完成定义:

- AI tools 有自己的 connector pack，证明 registry 跨领域。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
