# Round ID: OSS-3-R03

Round Name: Skill Replacement And Capability Handoff Proposal

本轮目标:

定义当发现更好的 skill/agent/framework 时，如何建议替换、补强或下线现有能力，而不是盲目叠加。

本轮任务:
- 执行任务:
  - 定义 replacement decision：keep、augment、replace_candidate、deprecate_candidate、story_only。
  - 输出 `artifacts/oss_research/capability_handoff_candidates.json`。
  - 每个候选必须包含 current_capability、new_candidate、decision_reason、migration_cost、verification_needed、handoff_target=CAP。
  - 对适合做内容的候选同时输出 `story_handoff=true` 和 content_angle。
- 测试任务:
  - 验证 handoff JSON 可解析。
  - 验证 replace_candidate 不会自动替换能力。
  - 验证 story_handoff 可以被 STORY 消费。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-3-R03.md`。
  - 生成 `.piko/summaries/worker_OSS-3.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/oss_research/*`
- `.piko/summaries/worker_OSS-3-R03.md`
- `.piko/summaries/worker_OSS-3.md`
- `.piko/round_status.json`

禁止修改:

- 不要自动替换能力。
- 不要删除旧能力。
- 不要发布内容。

必须运行的验证:

- Capability handoff JSON parse probe。
- No auto-replace guardrail scan。

完成定义:

- OSS 能把新发现分流给 CAP 和 STORY，但不直接变更生产能力。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
