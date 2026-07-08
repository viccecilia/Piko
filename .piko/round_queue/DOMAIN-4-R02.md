# Round ID: DOMAIN-4-R02

Round Name: Domain-Agnostic Workflow Contract

本轮目标:

让 workflow 使用通用阶段名，而不是游戏专属名。

本轮任务:
- 执行任务:
  - 定义 domain-agnostic workflow contract。
  - 阶段使用 collect_signals、cluster_needs、rank_opportunities、build_evidence、create_content_package、verify_gate。
  - 将 gaming 和 ai_tools fixture 都映射到该 workflow。
- 测试任务:
  - 测试 gaming workflow trace。
  - 测试 ai_tools workflow trace。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-4-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/domain_plugins/*`
- `.piko/summaries/worker_DOMAIN-4-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不删除 V05 LangGraph backend smoke。

必须运行的验证:

- Domain-agnostic workflow tests

完成定义:

- 同一 workflow contract 可跑两个领域。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
