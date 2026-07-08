# Round ID: LIVE-CONNECTOR-5-R01

Round Name: Operator Live Connector Surface

本轮目标:

让 operator 看见 live connector 的选择、approval、endpoint readiness、probe status、handoff status。

本轮任务:
- 执行任务:
  - 新增或扩展 API/window。
  - 展示 connector_id、status、real_collection_performed、blocked_reason、normalized_counts、handoff_status、ranking_preview_status。
  - Surface 只读，不触发 live collection。
- 测试任务:
  - API/window probe 如果实现。
  - HTML 无外部 URL/CDN。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-CONNECTOR-5-R01.md`。

允许修改:

- `apps/*`
- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/live_connector_pilot/*`
- `.piko/summaries/worker_LIVE-CONNECTOR-5-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不让窗口执行 live probe。

必须运行的验证:

- Operator live connector surface tests

完成定义:

- 人可以看懂 live connector 当前成功/阻断状态。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
