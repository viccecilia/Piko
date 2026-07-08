# Round ID: SOURCE-PROVIDER-5-R01

Round Name: Source Provider Operator Surface

本轮目标:

让 operator 能看到 source provider 状态、待部署包、外部 URL 验证状态和下一步动作。

本轮任务:
- 执行任务:
  - 新增或扩展 API/window。
  - 展示 provider_status、package_path、external_provider_validated、approved_url_redacted、next_action。
  - Surface 只读。
- 测试任务:
  - API/window probe 如果实现。
  - HTML 无外部 URL/CDN。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SOURCE-PROVIDER-5-R01.md`。

允许修改:

- `apps/*`
- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/source_provider/*`
- `.piko/summaries/worker_SOURCE-PROVIDER-5-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不让窗口上传/部署。

必须运行的验证:

- Source provider surface tests

完成定义:

- operator 能看懂外部 endpoint 准备到哪一步。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
