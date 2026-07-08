# Round ID: DOMAIN-1-R03

Round Name: Generic Signal And Need Contract

本轮目标:

把 game/player/question 等具体概念抽象为 generic signal 和 need cluster，避免 core 绑定游戏。

本轮任务:
- 执行任务:
  - 定义 GenericSourceSignal、NeedCluster、OpportunityScore、EvidenceTrace 的通用 contract。
  - 保留 domain_payload 用于领域专属字段。
  - 增加 migration map：GameHeatSignal -> GenericSourceSignal，PlayerQuestionSignal -> NeedCluster。
- 测试任务:
  - 测试 gaming signals 可映射到 generic contract。
  - 测试 ai_tools fixture 也可映射。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-1-R03.md` 和 `.piko/summaries/worker_DOMAIN-1.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/domain_plugins/*`
- `.piko/summaries/worker_DOMAIN-1-R03.md`
- `.piko/summaries/worker_DOMAIN-1.md`
- `.piko/round_status.json`

禁止修改:

- 不破坏现有 discovery tests。

必须运行的验证:

- Generic signal mapping tests

完成定义:

- Core 可处理通用领域信号，不依赖游戏名词。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
