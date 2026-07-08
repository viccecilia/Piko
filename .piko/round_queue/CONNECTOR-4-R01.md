# Round ID: CONNECTOR-4-R01

Round Name: Collection Plan Builder

本轮目标:

根据 domain 和目标，生成 collection plan，而不是直接采集。

本轮任务:
- 执行任务:
  - 生成 collection plan builder。
  - Plan 包含 domain_id、target_need、candidate_connectors、required_env、approval_status、expected_outputs、blocked_reasons。
  - 默认 mode=dry_run。
- 测试任务:
  - 测试 gaming plan。
  - 测试 ai_tools plan。
  - 测试 missing env -> blocked_for_endpoint。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-4-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不执行真实采集。

必须运行的验证:

- Collection plan tests

完成定义:

- Piko 能先计划数据采集，再由审批决定是否执行。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
