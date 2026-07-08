# Round ID: DOMAIN-3-R02

Round Name: AI Tools Fixture Signals

本轮目标:

为 ai_tools domain pack 创建 fixture signals，证明非游戏领域也能进入 generic signal/need pipeline。

本轮任务:
- 执行任务:
  - 创建 ai_tools fixture signals。
  - 包含至少 3 个工具/项目，2 个 need clusters。
  - 输出 normalized generic signals artifact。
- 测试任务:
  - 测试 ai_tools fixture 可映射 GenericSourceSignal 和 NeedCluster。
  - 测试 no real_collection_performed。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-3-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `fixtures/*`
- `artifacts/domain_plugins/*`
- `.piko/summaries/worker_DOMAIN-3-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不伪装真实 GitHub scan。

必须运行的验证:

- AI tools fixture mapping tests

完成定义:

- ai_tools 可走通通用信号层。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
