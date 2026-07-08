# Round ID: CAP-3-R03

Round Name: Autonomous Run Report

本轮目标:

建立自动运行报告，让 Piko 每次自动执行后能把“做了什么、用了哪些能力、验证结果、需要人类确认什么”交给操作员。

本轮任务:
- 执行任务:
  - 定义 autonomous run report artifact：run_id、objective、capabilities_used、fallbacks_used、outputs、tests_run、verification_status、human_approval_required、next_actions。
  - 生成 sample report `artifacts/capability_map/latest_autonomous_run_report.json`。
  - 报告必须明确 no_publish/no_deploy 状态。
- 测试任务:
  - report JSON 可解析。
  - report 包含 capabilities_used 和 human_approval_required。
  - no publish/deploy side effects。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-3-R03.md`。
  - 生成 `.piko/summaries/worker_CAP-3.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_CAP-3-R03.md`
- `.piko/summaries/worker_CAP-3.md`
- `.piko/round_status.json`

禁止修改:

- 不要自动发布或部署。
- 不要自动批准 human approval item。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- autonomous run report JSON parse probe

完成定义:

- CAP-3 三个 round summary 和 stage summary 存在。
- 自动运行边界和人类确认合同可被审阅。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
