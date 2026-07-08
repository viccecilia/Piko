# Round ID: FINISH-5-R01
Round Name: Publish Distribution Dry-Run Package

本轮目标:

生成一键发布前的多平台 distribution plan，但默认 dry-run，不上传、不发布、不保存凭据。

本轮任务:
- 执行任务:
  - 为小红书、公众号、抖音/短视频、网站输出 platform-specific package。
  - 生成 payload preview、required credentials list、approval checklist。
  - 输出 `artifacts/final_mvp/latest_publish_distribution_plan.json`。
- 测试任务:
  - 测试 dispatch_performed=false、upload_performed=false、publishing_performed=false。
  - 测试 credential_storage_performed=false。
  - 测试每个平台有 required approval gate。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_FINISH-5-R01.md`。

允许修改:

- `packages/final_mvp/**`
- `packages/skills/**`
- `tests/**`
- `artifacts/final_mvp/**`

禁止修改:

- 不得调用真实平台 API。
- 不得保存平台 token。
- 不得真实上传图片/视频/文章。

必须运行的验证:

- distribution dry-run 专项测试
- structured guardrail scan

完成定义:

- 人类能看到“一键发布前准备好了什么”。
- 所有真实发布动作均为 false。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

