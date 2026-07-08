# Round ID: CAP-3-R02

Round Name: Human Final Approval Contract

本轮目标:

定义最终人类确认合同，明确什么情况下系统必须停下等待确认。

本轮任务:
- 执行任务:
  - 定义 human approval contract：approval_id、action_type、summary、evidence_links、risk_flags、rollback_plan、expires_at、operator_decision。
  - 覆盖 action types：publish_article、deploy_site、use_paid_api、store_credentials、replace_capability、vendor_dependency、change_guardrail。
  - 输出 `artifacts/capability_map/human_approval_contract.json`。
  - 文档说明：系统可以自动准备材料，但最后确认必须由人类做。
- 测试任务:
  - approval contract JSON 可解析。
  - 高风险 action 必须包含 rollback_plan 和 evidence_links。
  - 未批准 action 不得执行。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-3-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_CAP-3-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要实现真实 publish/deploy approval action。
- 不要自动批准。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- approval contract JSON parse probe

完成定义:

- 最终人类确认合同清晰。
- 系统知道何时必须停下。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
