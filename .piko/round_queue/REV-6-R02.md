# Round ID: REV-6-R02

Round Name: Media Plan And Publish Readiness Metadata

本轮目标:

为 internal article package 增加配图/媒体计划和发布准备元数据，让操作员知道文章还缺什么素材、哪些素材可以安全使用、为什么目前能或不能发布。

本轮任务:
- 执行任务:
  - 新增 media plan 字段：recommended_media、required_screenshots、image_source_policy、alt_text、license/safety notes。
  - 不下载、不抓取、不复制外部图片；只生成安全素材需求和来源策略。
  - 增加 publish readiness metadata：verification_status、source_trace_present、evidence_trace_present、media_plan_present、manual_publish_required、publishing_performed=false。
  - 若文章缺图，明确 `has_images=false` 但 `media_plan_present=true`。
- 测试任务:
  - Article package 或 publish readiness artifact 包含 media plan。
  - 不存在外部图片下载副作用。
  - publish readiness 不等于 publish approval。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-6-R02.md`。

允许修改:

- `packages/workflows/*`
- `packages/discovery/*`
- `artifacts/article_drafts/*`
- `artifacts/publish_readiness/*`
- `tests/test_discovery_search.py`
- `docs/current_state.md`
- `.piko/summaries/worker_REV-6-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要下载或保存外部图片。
- 不要抓取地图、截图或网页图片。
- 不要真实发布或部署。
- 不要把 publish readiness 标成 publish performed。
- 不要默认调用 LLM 或 image generation。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- publish readiness artifact probe

完成定义:

- 文章包有媒体计划和发布准备字段。
- 系统能回答“还缺哪些图/素材”和“为什么还不能一键发布”。
- 没有图片抓取/发布副作用。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
