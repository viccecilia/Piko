# Round ID: LIVE-CONNECTOR-2-R03

Round Name: Bounded Live Collection Artifact

本轮目标:

将 endpoint verification 结果写成 bounded live collection artifact。成功才允许 real_collection_performed=true。

本轮任务:
- 执行任务:
  - 生成 bounded live collection artifact。
  - 字段包含 status、connector_id、real_collection_performed、normalized_counts、payload_size_bounds、raw_body_saved=false、publishing_performed=false。
  - 若 blocked，明确 blocked_reason。
- 测试任务:
  - 测试 success/blocked 字段一致。
  - 测试 raw_body_saved=false。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-CONNECTOR-2-R03.md` 和 `.piko/summaries/worker_LIVE-CONNECTOR-2.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/live_connector_pilot/*`
- `.piko/summaries/worker_LIVE-CONNECTOR-2-R03.md`
- `.piko/summaries/worker_LIVE-CONNECTOR-2.md`
- `.piko/round_status.json`

禁止修改:

- 不把 blocked 写成 success。

必须运行的验证:

- Bounded live collection artifact tests

完成定义:

- live collection 状态可机读、可验证、可追责。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
