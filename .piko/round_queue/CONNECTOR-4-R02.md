# Round ID: CONNECTOR-4-R02

Round Name: Collection Dry Run Report

本轮目标:

执行 collection dry-run report，展示如果要采集会调用哪些 connector、缺什么、会保留什么字段。

本轮任务:
- 执行任务:
  - 生成 dry-run report artifact。
  - 包含 no_network_performed=true、connectors_planned、blocked_connectors、retained_fields、prohibited_fields。
  - 展示 REAL 当前缺 endpoint 的状态。
- 测试任务:
  - 测试 no_network_performed=true。
  - 测试 dry-run 不写 real_collection_performed=true。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-4-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-4-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不触网。
- 不调用 connector search。

必须运行的验证:

- Collection dry-run tests

完成定义:

- Operator 能看到采集计划，但没有真实采集副作用。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
