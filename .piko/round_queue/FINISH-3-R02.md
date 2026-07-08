# Round ID: FINISH-3-R02
Round Name: Content Quality Package And Media Plan

本轮目标:

生成可供人类审核的高质量内容包：标题、正文结构、摘要、证据说明、平台改写、图片/媒体计划，但不发布。

本轮任务:
- 执行任务:
  - 复用 content quality skill 输出标题候选、正文、短视频脚本、小红书/公众号适配。
  - 生成 media_plan，但不下载、不生成、不上传图片。
  - 输出 `latest_content_package.json` 的 final package section。
- 测试任务:
  - 测试 package 包含 evidence、quality_score、platform_adaptations。
  - 测试 media_plan_present=true 但 image_generation_performed=false。
  - 测试 publish_ready=false、publishing_performed=false。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_FINISH-3-R02.md` 和 `.piko/summaries/worker_FINISH-3.md`。

允许修改:

- `packages/final_mvp/**`
- `packages/skills/**`
- `packages/storytelling/**`
- `tests/**`
- `artifacts/final_mvp/**`

禁止修改:

- 不得克隆真人声音。
- 不得引用外部 CDN。
- 不得上传或发布内容。

必须运行的验证:

- content package 专项测试
- STORY/HTML guardrail scan if HTML generated

完成定义:

- 内容包可审核、可追溯、可分发准备。
- 所有发布副作用为 false。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

