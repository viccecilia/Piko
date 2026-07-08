# Round ID: STORY-0-R01

Round Name: Fixed Storytelling Skill Contract

本轮目标:

把 `agent-skill-storytelling` 固定为 Piko 每日 agent/skill/open-source capability 图文和视频内容的默认表达结构。

本轮任务:
- 执行任务:
  - 检查 `C:\Users\pangv\.codex\skills\agent-skill-storytelling\SKILL.md` 是否存在。
  - 确认 skill description 能覆盖 agent、skill、open-source capability、Piko capability introduction 这类内容。
  - 确认固定结构存在：强标题、旧痛点、新能力、快速判断、机制解释、实操步骤、真实限制、适合谁、总结和行动。
  - 记录当前结构版本，例如 `storytelling_template_version=v1`。
- 测试任务:
  - 运行 skill validation。
  - 检查 reference 文件存在：`story-structure.md`、`video-package.md`。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_STORY-0-R01.md`。

允许修改:

- `C:\Users\pangv\.codex\skills\agent-skill-storytelling\*`
- `artifacts/storytelling/*`
- `tests/*`
- `docs/*`
- `.piko/summaries/worker_STORY-0-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要推翻默认结构；本轮只允许修复缺失字段。
- 不要发布或上传任何内容。
- 不要克隆真人声线。
- 不要使用未经许可的外部图片。

必须运行的验证:

- `python C:\Users\pangv\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\pangv\.codex\skills\agent-skill-storytelling`

完成定义:

- 固定 storytelling skill 可用且结构明确。
- 后续每日内容默认使用该 skill。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
