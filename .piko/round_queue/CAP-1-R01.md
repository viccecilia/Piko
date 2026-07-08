# Round ID: CAP-1-R01

Round Name: Capability Evaluation Metrics

本轮目标:

建立能力评分标准，用于判断一个 agent/skill/tool 是保留、改进、包装、替换还是淘汰。

本轮任务:
- 执行任务:
  - 定义 capability score components：accuracy、reliability、cost、latency、maintainability、security、license safety、domain fit、test coverage、operator ergonomics。
  - 每个 component 定义 0-100 分含义。
  - 生成 `artifacts/capability_map/capability_evaluation_policy.json`。
- 测试任务:
  - policy JSON 可解析。
  - 每个 component 有说明和权重。
  - replacement decision 不允许只看单一指标。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-1-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_CAP-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要替换实际能力。
- 不要安装外部工具。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- policy artifact JSON parse probe

完成定义:

- Capability evaluation policy 存在。
- 替换/淘汰有明确评分依据。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
