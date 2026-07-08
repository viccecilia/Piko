# Round ID: STORY-3-R03

Round Name: HyperFrames Video Draft

本轮目标:

用本地 HTML/HyperFrames 风格生成短视频草稿页面，供人工预览和后续渲染。

本轮任务:
- 执行任务:
  - 生成或更新 `artifacts/storytelling/latest_video/index.html`。
  - 使用 latest storyboard、voiceover、copy package 作为输入。
  - 页面应为竖屏短视频草稿，包含标题、关键步骤、机制解释、限制提醒、结尾行动。
  - 使用本地素材；如无素材，用抽象卡片、流程图、代码片段、能力图视觉替代。
- 测试任务:
  - 检查 HTML 存在且可打开。
  - 检查页面包含今日 candidate 名称和主要段落。
  - 检查没有外链到未经授权媒体。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_STORY-3-R03.md`。
  - 生成 `.piko/summaries/worker_STORY-3.md`。

允许修改:

- `artifacts/storytelling/*`
- `.piko/summaries/worker_STORY-3-R03.md`
- `.piko/summaries/worker_STORY-3.md`
- `.piko/round_status.json`

禁止修改:

- 不要上传视频。
- 不要自动渲染并发布。
- 不要调用外部图片生成或 TTS，除非后续专门 round 显式允许。

必须运行的验证:

- HTML existence probe。
- Local media/link safety probe。

完成定义:

- 已生成可预览的本地视频草稿页面，但仍是 draft。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
