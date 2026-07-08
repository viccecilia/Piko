# Round ID: OSS-2-R02

Round Name: Piko Upgrade Proposal Mapping

本轮目标:

把架构模式映射成 Piko 可执行但未自动应用的升级提案。

本轮任务:
- 执行任务:
  - 读取 `latest_patterns.json`。
  - 输出 `artifacts/oss_research/latest_upgrade_proposals.json`。
  - 每个 proposal 至少包含 proposal_id、target_area、expected_benefit、implementation_shape、tests_needed、rollback_plan、handoff_target。
  - handoff_target 可为 CAP、STORY、WORKER_QUEUE、none。
  - 对 STORY 友好的项目要输出 content_angle。
- 测试任务:
  - 验证 proposal JSON 可解析。
  - 验证每个 proposal 有 tests_needed 和 rollback_plan。
  - 验证 proposals 不会自动应用 patch。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-2-R02.md`。
  - 生成 `.piko/summaries/worker_OSS-2.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/oss_research/*`
- `.piko/summaries/worker_OSS-2-R02.md`
- `.piko/summaries/worker_OSS-2.md`
- `.piko/round_status.json`

禁止修改:

- 不要自动改 runtime 行为。
- 不要自动安装新框架。
- 不要发布或部署。

必须运行的验证:

- Upgrade proposal JSON parse probe。
- Auto-apply guardrail scan。

完成定义:

- OSS-2 产生可审查的 Piko 升级提案，并能分流到 CAP/STORY。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
