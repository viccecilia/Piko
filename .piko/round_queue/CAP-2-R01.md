# Round ID: CAP-2-R01

Round Name: Capability Registry Schema

本轮目标:

建立统一 capability registry schema，让 Piko 能结构化记录 agent、skill、connector、workflow、domain plugin 和 UI surface。

本轮任务:
- 执行任务:
  - 定义 registry schema：capability_id、name、kind、provider、status、inputs、outputs、domains、cost_class、network_policy、requires_credentials、tests、fallbacks、owner。
  - 支持 kinds：local_agent、workflow、skill、connector、mcp_tool、domain_plugin、operator_surface、automation。
  - 输出 `artifacts/capability_map/capability_registry.json`。
- 测试任务:
  - registry JSON 可解析。
  - 每个 capability 有 network_policy 和 fallback。
  - requires_credentials 为 true 的能力不得默认启用。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-2-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_CAP-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要自动调用 credentials-required 能力。
- 不要安装新 connector。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- registry JSON parse probe

完成定义:

- Capability registry schema 和第一版 registry 存在。
- 能力可被机器读取和人类审阅。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
