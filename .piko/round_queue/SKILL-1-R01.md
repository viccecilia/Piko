# Round ID: SKILL-1-R01

Round Name: Skill Manifest And Trigger Contract

本轮目标:

建立 Piko Skill Runtime v0 的 manifest 与 trigger contract，吸收 Superpowers / DeerFlow / mem0 的 skill 管理模式，但不依赖外部项目。

本轮任务:
- 执行任务:
  - 定义 skill manifest schema：skill_id、version、purpose、triggers、inputs、outputs、risk_level、owner、eval_suite、activation_status。
  - 定义 progressive loading policy：只加载匹配任务的 skill，不全量加载。
  - 生成 skill runtime registry artifact。
- 测试任务:
  - 测试 manifest 必填字段。
  - 测试 activation_status 默认 candidate。
  - 测试 trigger matching 不自动执行 skill。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-1-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/skill_runtime/*`
- `.piko/summaries/worker_SKILL-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不安装外部 skill。
- 不自动激活 candidate skill。

必须运行的验证:

- Skill manifest tests

完成定义:

- Piko 有可验证的 Skill Runtime v0 manifest/trigger contract。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
