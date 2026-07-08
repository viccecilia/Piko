# Round ID: ENDPOINT-3-R02

Round Name: Normalize Successful Live Signals

本轮目标:

将 live success payload normalize 成 generic/domain signals，并生成可供 REAL 使用的 artifact。

本轮任务:
- 执行任务:
  - 生成 normalized live signals success artifact。
  - 包含 games/signals/questions/need_clusters counts 和 source trace。
  - 保持 bounded snippets。
- 测试任务:
  - 测试 real_collection_performed=true 与 evidence 一致。
  - 测试 prohibited fields 不出现。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_ENDPOINT-3-R02.md` 和 `.piko/summaries/worker_ENDPOINT-3.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/live_connector_pilot/*`
- `artifacts/local_endpoint/*`
- `.piko/summaries/worker_ENDPOINT-3-R02.md`
- `.piko/summaries/worker_ENDPOINT-3.md`
- `.piko/round_status.json`

禁止修改:

- 不伪造 external coverage。

必须运行的验证:

- Successful live normalization tests

完成定义:

- live success 数据可以进入通用信号层。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
