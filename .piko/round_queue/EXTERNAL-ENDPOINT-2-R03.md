# Round ID: EXTERNAL-ENDPOINT-2-R03

Round Name: External Collection Safety Summary

本轮目标:

生成外部采集安全摘要，证明没有保存 raw/full source 或敏感值。

本轮任务:
- 执行任务:
  - 生成 safety summary artifact。
  - 字段包含 raw_response_body_saved=false、full_posts_saved=false、secrets_retained=false、crawler_used=false、broad_internet_coverage=false。
  - 成功时 real_collection_performed=true；blocked/failed 时 false。
- 测试任务:
  - 测试安全字段。
  - 测试 blocked 不写 success。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-2-R03.md` 和 `.piko/summaries/worker_EXTERNAL-ENDPOINT-2.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/external_endpoint/*`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-2-R03.md`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-2.md`
- `.piko/round_status.json`

禁止修改:

- 不伪造 success。

必须运行的验证:

- External collection safety tests

完成定义:

- 外部采集安全状态可验证。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
