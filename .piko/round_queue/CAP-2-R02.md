# Round ID: CAP-2-R02

Round Name: Capability Routing Policy

本轮目标:

定义任务到能力的路由策略，让 Piko 能选择合适 agent/skill/tool，并在能力不可用时使用 fallback。

本轮任务:
- 执行任务:
  - 定义 routing policy：task_type -> preferred capabilities -> fallback capabilities -> forbidden capabilities。
  - 覆盖 task types：market_discovery、source_collection、evidence_extraction、ranking、writing、editing、factcheck、verification、dashboard、document_export、security_review、github_research。
  - 定义 routing constraints：default_no_network、credential_required、human_approval_required、license_sensitive。
  - 输出 `artifacts/capability_map/capability_routing_policy.json`。
- 测试任务:
  - routing policy JSON 可解析。
  - 每个 task_type 至少有 preferred 或 fallback。
  - forbidden capabilities 不会被默认选择。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-2-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_CAP-2-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要改变 runtime routing 默认行为，除非测试证明兼容。
- 不要默认联网。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- routing policy JSON parse probe

完成定义:

- Piko 有任务到能力的可解释路由策略。
- fallback 和 forbidden rules 明确。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
