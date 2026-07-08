# Round ID: REAL-4-R02

Round Name: Publish Readiness And Media Plan

本轮目标:

生成 publish readiness 和 media plan，但保持一键发布前候选，不实际发布、不生成/下载图片。

本轮任务:
- 执行任务:
  - 生成 publish readiness artifact。
  - 生成 media plan artifact：需要哪些图、来源策略、版权风险、是否已有图片=false。
  - 明确 one_click_publish_ready=false 或 human_approval_required=true。
- 测试任务:
  - 测试 publishing_performed=false。
  - 测试 has_images=false，image_generation_performed=false。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REAL-4-R02.md` 和 `.piko/summaries/worker_REAL-4.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/publish_readiness/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_REAL-4-R02.md`
- `.piko/summaries/worker_REAL-4.md`
- `.piko/round_status.json`

禁止修改:

- 不发布。
- 不下载图片。
- 不调用 image generation。

必须运行的验证:

- Publish readiness safety tests

完成定义:

- 候选内容清楚说明离发布还差人工确认和媒体素材。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
