# Round ID: EXTERNAL-ENDPOINT-5-R01

Round Name: Operator External Endpoint Surface

本轮目标:

让 operator 看见外部 endpoint 状态：approval、readiness、HTTP probe、contract validation、REAL handoff、article candidate。

本轮任务:
- 执行任务:
  - 新增或扩展 API/window。
  - 展示 scope、real_collection_performed、broad_internet_coverage=false、blocked_reason、normalized_counts、candidate_status。
  - Surface 只读。
- 测试任务:
  - API/window probe 如果实现。
  - HTML 无外部 URL/CDN。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-5-R01.md`。

允许修改:

- `apps/*`
- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/external_endpoint/*`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-5-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不让窗口触发外部请求或发布。

必须运行的验证:

- Operator external endpoint surface tests

完成定义:

- 人能看懂 external endpoint 成功/阻断状态和范围。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
