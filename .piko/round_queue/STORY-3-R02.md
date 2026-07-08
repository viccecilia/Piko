# Round ID: STORY-3-R02

Round Name: Storyboard And Screen Text

本轮目标:

把口播稿拆成短视频分镜、屏幕文字、视觉节奏和素材需求。

本轮任务:
- 执行任务:
  - 生成 `artifacts/storytelling/latest_storyboard.md`。
  - 至少包含 6-10 个镜头，每个镜头有 narration、on_screen_text、visual_direction、duration_seconds。
  - 使用本地已授权素材或抽象 UI/代码/流程图视觉，不依赖外部未授权图片。
- 测试任务:
  - 检查分镜数量。
  - 检查每个镜头都有口播和屏幕文字。
  - 检查没有要求下载版权图片。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_STORY-3-R02.md`。

允许修改:

- `artifacts/storytelling/*`
- `.piko/summaries/worker_STORY-3-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要下载外部图片或视频。
- 不要生成平台发布文件。

必须运行的验证:

- Storyboard completeness probe。

完成定义:

- 分镜能直接指导生成 HTML 视频草稿。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
