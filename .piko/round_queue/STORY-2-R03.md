# Round ID: STORY-2-R03

Round Name: Copy Package Artifact

本轮目标:

把公众号、小红书、标题候选、封面文案、来源和风险说明合并成统一内容包。

本轮任务:
- 执行任务:
  - 生成 `artifacts/storytelling/latest_copy_package.json`。
  - 至少包含 title_options、wechat_article_path、xiaohongshu_path、cover_copy、source_refs、risk_notes、publish_ready=false。
  - 保留 `template_version` 和 candidate metadata。
- 测试任务:
  - 验证 JSON 可解析。
  - 验证 `publish_ready=false`。
  - 验证 source_refs 不为空；无来源时必须标记为 `source_gap=true`。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_STORY-2-R03.md`。
  - 生成 `.piko/summaries/worker_STORY-2.md`。

允许修改:

- `artifacts/storytelling/*`
- `.piko/summaries/worker_STORY-2-R03.md`
- `.piko/summaries/worker_STORY-2.md`
- `.piko/round_status.json`

禁止修改:

- 不要把 copy package 标记为已发布。
- 不要发布到任何平台。

必须运行的验证:

- Copy package JSON parse probe。

完成定义:

- STORY-2 完整输出可交给视频生成 round 使用。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
