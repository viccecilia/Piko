# Round ID: STORY-2-R01

Round Name: WeChat Article Draft

本轮目标:

按固定结构生成一篇公众号图文文案草稿，用于介绍今日 agent/skill/capability。

本轮任务:
- 执行任务:
  - 读取 `latest_candidate_selection.json` 和 active template。
  - 生成 `artifacts/storytelling/latest_wechat_article.md`。
  - 文案必须包含：标题钩子、痛点引入、能力解释、判断标准、实操步骤、限制、适合人群、总结行动。
  - 所有事实性描述必须关联 source_refs 或标记为推断。
- 测试任务:
  - 检查九段结构完整。
  - 检查没有“确定能自动赚钱/保证爆款/完全替代人工”等夸大表达。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_STORY-2-R01.md`。

允许修改:

- `artifacts/storytelling/*`
- `docs/*`
- `.piko/summaries/worker_STORY-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要发布到公众号。
- 不要复制外部文章全文或长段落。
- 不要伪造来源。

必须运行的验证:

- WeChat draft structure probe。

完成定义:

- 公众号草稿可读、结构完整、风险表达克制。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
