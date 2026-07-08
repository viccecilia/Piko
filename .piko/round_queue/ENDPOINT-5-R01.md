# Round ID: ENDPOINT-5-R01

Round Name: Operator Endpoint Result Surface

本轮目标:

让 operator 看到本地 approved endpoint success path：endpoint smoke、live success、normalized counts、REAL handoff、article handoff。

本轮任务:
- 执行任务:
  - 新增或扩展 endpoint result API/window。
  - 展示 scope=local_approved_endpoint、real_collection_performed=true、broad_internet_coverage=false。
  - Surface 只读。
- 测试任务:
  - API/window probe 如果实现。
  - HTML 无外部 URL/CDN。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_ENDPOINT-5-R01.md`。

允许修改:

- `apps/*`
- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/local_endpoint/*`
- `.piko/summaries/worker_ENDPOINT-5-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不让窗口触发发布/采集。

必须运行的验证:

- Operator endpoint result tests

完成定义:

- 人能看懂这次成功是本地 approved endpoint 成功，不是全网。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
