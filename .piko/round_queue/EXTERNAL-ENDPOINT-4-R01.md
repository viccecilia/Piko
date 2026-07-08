# Round ID: EXTERNAL-ENDPOINT-4-R01

Round Name: REAL Funnel External Handoff

本轮目标:

将 external normalized signals 接入 REAL funnel，生成 external scope 的 candidates/pain buckets；blocked 时保持 blocked。

本轮任务:
- 执行任务:
  - 生成 REAL external handoff artifact。
  - 成功时包含 top candidates、pain buckets、source trace。
  - blocked/failed 时包含 reason。
  - 不生成 publish approval。
- 测试任务:
  - 测试 handoff 状态与 real_collection_performed 一致。
  - 测试不声称 broad internet coverage。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-4-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/external_endpoint/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不伪造 Top 5。

必须运行的验证:

- REAL external handoff tests

完成定义:

- 外部 endpoint 可进入 REAL 漏斗，或被安全阻断。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
