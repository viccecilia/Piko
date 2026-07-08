# Round ID: OSS-3-R02

Round Name: Domain Plugin Upgrade Proposal

本轮目标:

让 Piko 从游戏领域扩展为可插拔领域模板，外部开源经验可以映射到不同 domain plugin。

本轮任务:
- 执行任务:
  - 设计 DomainPlugin 接口草案，至少包含 domain_id、source_connectors、topic_scorers、evidence_rules、writer_profile、verification_rules、publish_policy。
  - 输出 gaming domain migration plan，要求不破坏现有游戏 discovery。
  - 输出一个 non-gaming demo domain 设计，例如 AI tools、local services、software troubleshooting、travel guide 中任选一个。
  - 保存 `artifacts/oss_research/domain_plugin_proposal.json`。
- 测试任务:
  - 验证 proposal JSON 可解析。
  - 验证 gaming 为默认兼容 domain。
  - 验证 demo domain 不触发真实联网或发布。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-3-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/oss_research/*`
- `.piko/summaries/worker_OSS-3-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要破坏 gaming 现有行为。
- 不要新增真实采集默认路径。
- 不要发布、部署。

必须运行的验证:

- Domain plugin proposal JSON parse probe。
- Existing discovery tests。

完成定义:

- Piko 的可插拔领域方向被结构化为 proposal。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
