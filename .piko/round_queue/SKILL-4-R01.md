# Round ID: SKILL-4-R01

Round Name: Content Quality Rubric

本轮目标:

建立 Piko 产出物文案质量评分标准，重点提升爆款标题、抓人引言、结构清晰度、证据可信度和平台适配。

本轮任务:
- 执行任务:
  - 定义 content quality rubric artifact。
  - 评分维度至少包含 hook_strength、reader_pain_match、clarity、evidence_trace、platform_fit、actionability、risk_disclosure。
  - 支持小红书、公众号、抖音口播稿三种输出格式。
- 测试任务:
  - 测试 rubric 字段完整。
  - 测试低质量草稿能得到明确改进建议。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-4-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/content_quality/*`
- `.piko/summaries/worker_SKILL-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不调用真实 LLM。
- 不使用未经授权图片。

必须运行的验证:

- Content quality rubric tests

完成定义:

- Piko 有明确可测的内容质量标准。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
