# Round ID: STORY-0-R02

Round Name: Storytelling Template Registry

本轮目标:

建立 storytelling template registry，记录当前默认结构和未来候选结构，避免每天风格漂移。

本轮任务:
- 执行任务:
  - 生成 `artifacts/storytelling/template_registry.json`。
  - Registry 至少包含 `template_id`、`version`、`source_reference`、`structure`、`allowed_outputs`、`guardrails`、`status`。
  - 默认 active template 必须是 `agent-skill-storytelling:v1`。
  - 状态枚举建议为 `active`、`candidate`、`deprecated`。
- 测试任务:
  - 验证 registry JSON 可解析。
  - 验证 active template 只有一个。
  - 验证 active template 包含固定结构九段。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_STORY-0-R02.md`。
  - 生成 `.piko/summaries/worker_STORY-0.md`。

允许修改:

- `artifacts/storytelling/*`
- `packages/*`
- `tests/*`
- `docs/*`
- `.piko/summaries/worker_STORY-0-R02.md`
- `.piko/summaries/worker_STORY-0.md`
- `.piko/round_status.json`

禁止修改:

- 不要新增未经讨论的 active template。
- 不要发布或上传内容。

必须运行的验证:

- Registry JSON parse probe。

完成定义:

- STORY-0 summaries 存在。
- Storytelling template registry 可用于每日内容生成。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
