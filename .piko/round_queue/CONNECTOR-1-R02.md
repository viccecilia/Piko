# Round ID: CONNECTOR-1-R02

Round Name: Connector Manifest Examples

本轮目标:

为已知 connector 类型创建 manifest examples，覆盖 approved_json_endpoint、mediawiki、steam、reddit、serp、github_repo 等。

本轮任务:
- 执行任务:
  - 生成 connector manifest examples artifact。
  - 每个 manifest 标明 retained/prohibited fields 和默认状态。
  - approved_json_endpoint 作为跨 domain 通用 connector。
- 测试任务:
  - 测试所有示例 manifest 可通过 registry contract。
  - 测试 prohibited fields 包含 raw/full source 与 credentials。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-1-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-1-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不调用真实 endpoint。

必须运行的验证:

- Connector manifest tests

完成定义:

- 常见 connector 类型有可验证 manifest。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
