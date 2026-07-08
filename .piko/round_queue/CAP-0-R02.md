# Round ID: CAP-0-R02

Round Name: Available Skills And Connector Inventory

本轮目标:

盘点当前 Codex 环境可用 skills、plugins、MCP/connectors、automation 能力，并标记哪些可直接用于 Piko。

本轮任务:
- 执行任务:
  - 记录当前可用 skills/categories，例如 browser、playwright、github、data analytics、documents、spreadsheets、imagegen、OpenAI docs、security、automation。
  - 记录每个 skill/connector 的用途、适合 Piko 的场景、风险、是否需要用户显式触发。
  - 输出 `artifacts/capability_map/external_tools_inventory.json`。
  - 明确区分：available_now、needs_install、needs_credentials、not_allowed_by_default。
- 测试任务:
  - artifact JSON 可解析。
  - 每个 tool/skill 记录 safety boundary。
  - 不调用需要凭证或付费的外部服务。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-0-R02.md`。

允许修改:

- `docs/*`
- `artifacts/capability_map/*`
- `tests/*`
- `.piko/summaries/worker_CAP-0-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要安装新插件。
- 不要请求 credentials。
- 不要调用 paid/external APIs。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- capability artifact JSON parse probe

完成定义:

- 当前 skills/connectors 能力被结构化记录。
- Piko 知道哪些能力可复用、哪些需要人工授权。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
