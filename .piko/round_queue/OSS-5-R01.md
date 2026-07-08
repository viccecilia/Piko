# Round ID: OSS-5-R01

Round Name: Daily Open Source Learning Operator Guide

本轮目标:

补全文档，说明每日 OSS 学习循环如何运行、如何和 CAP/STORY 配合、何时需要人工确认。

本轮任务:
- 执行任务:
  - 更新或新增 docs，说明每日流程：GitHub 扫描 -> OSS scoring -> pattern extraction -> CAP candidate -> STORY content candidate -> human review。
  - 明确 automation 只能生成研究和草稿，不自动安装依赖、不自动替换能力、不自动发布内容。
  - 说明如果当天没有新 skill，STORY 可以选择同类未覆盖 skill 做内容。
  - 说明真实 GitHub API 接入需要显式配置和验证。
- 测试任务:
  - 文档检查：包含 CAP、STORY、human final confirmation、no auto-apply、no auto-publish。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-5-R01.md`。

允许修改:

- `docs/*`
- `artifacts/oss_research/*`
- `.piko/summaries/worker_OSS-5-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要声称系统已完全自动升级。
- 不要声称已完成真实 GitHub 全网覆盖，除非有 live verification。

必须运行的验证:

- Docs keyword probe。

完成定义:

- 操作员能理解 OSS/CAP/STORY 的日常闭环和人工确认边界。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
