# Round ID: STORY-3-R01

Round Name: Voiceover Script And TTS Plan

本轮目标:

为今日内容生成口播稿和配音计划，声线方向可以接近知识类短视频，但不得克隆或冒充具体真人。

本轮任务:
- 执行任务:
  - 读取 latest copy package。
  - 生成 `artifacts/storytelling/latest_voiceover.md`。
  - 生成 `artifacts/storytelling/latest_tts_plan.json`。
  - 口播稿控制在 60-120 秒，语言直接、少废话、有停顿点。
  - TTS plan 只能描述声线风格，例如清晰、快节奏、知识讲解感，不得写“克隆某人声线”。
- 测试任务:
  - 检查 voiceover 存在。
  - 检查 TTS plan 无 voice cloning、impersonation、某真人姓名声线。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_STORY-3-R01.md`。

允许修改:

- `artifacts/storytelling/*`
- `.piko/summaries/worker_STORY-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要调用真实 TTS 服务。
- 不要克隆或冒充真人声音。
- 不要上传音频。

必须运行的验证:

- Voiceover/TTS plan guardrail probe。

完成定义:

- 有可用于后续视频草稿的口播稿和安全 TTS 计划。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
