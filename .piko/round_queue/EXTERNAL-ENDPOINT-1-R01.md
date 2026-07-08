# Round ID: EXTERNAL-ENDPOINT-1-R01

Round Name: External Endpoint Approval Contract

本轮目标:

建立外部 approved JSON endpoint 的 approval contract，明确它是 operator-approved external endpoint，不是 crawler 或任意网页。

本轮任务:
- 执行任务:
  - 生成 external endpoint approval artifact。
  - 字段包含 endpoint_required=true、endpoint_type=json、operator_approved_required=true、allowed_scope=external_approved_endpoint、broad_internet_coverage=false。
  - 明确 rejected endpoint types：html、rss、raw_body、crawler。
- 测试任务:
  - 测试 approval artifact 可解析。
  - 测试 broad_internet_coverage=false。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-1-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/external_endpoint/*`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不调用外部 endpoint。

必须运行的验证:

- External endpoint approval tests

完成定义:

- 外部 endpoint 的批准边界清楚且可机读。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
