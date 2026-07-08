# Round ID: CAP-1-R02

Round Name: Replacement And Deprecation Policy

本轮目标:

定义能力替换和淘汰政策，让 Piko 可以逐步换掉较差 skill/agent，但必须可回滚、可验证。

本轮任务:
- 执行任务:
  - 定义 replacement lifecycle：candidate -> shadow_test -> limited_rollout -> verified_replacement -> deprecated -> removed。
  - 定义何时允许替换：
    - 新能力评分显著更高
    - 兼容现有 contract
    - 测试覆盖充分
    - 回滚方案明确
    - license/security 可接受
  - 定义禁止替换场景：缺测试、license 不明、默认联网变更、删除 guardrail、绕过 verify。
  - 输出 `artifacts/capability_map/replacement_policy.json`。
- 测试任务:
  - policy JSON 可解析。
  - policy 包含 rollback、shadow_test、verification_required。
  - 高风险替换必须 requires_human_approval。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-1-R02.md`。

允许修改:

- `docs/*`
- `tests/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_CAP-1-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要实际 deprecate/remove 能力。
- 不要自动安装 replacement。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- replacement policy JSON parse probe

完成定义:

- 能力替换有生命周期和人工确认边界。
- Piko 不会自动换掉核心能力。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
