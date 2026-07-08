# Round ID: SKILL-4-R03

Round Name: Multi-Platform Content Package

本轮目标:

把内容质量引擎输出拆成小红书图文、公众号长文、抖音口播短视频脚本三套平台适配包。

本轮任务:
- 执行任务:
  - 生成 multi-platform content package。
  - 小红书：标题、封面文案、图卡大纲、正文、标签。
  - 公众号：标题、摘要、正文结构、配图建议。
  - 抖音：开场 3 秒、口播稿、分镜、字幕点。
- 测试任务:
  - 测试每个平台字段完整。
  - 测试 publish_ready=false、publishing_performed=false。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-4-R03.md` 和 `.piko/summaries/worker_SKILL-4.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/content_quality/*`
- `.piko/summaries/worker_SKILL-4-R03.md`
- `.piko/summaries/worker_SKILL-4.md`
- `.piko/round_status.json`

禁止修改:

- 不发布、不上传。

必须运行的验证:

- Multi-platform package tests

完成定义:

- 同一素材能产出三种平台候选内容包，但不发布。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
