# Round ID: STORY-1-R01

Round Name: Daily Skill Candidate Intake

本轮目标:

从每日 GitHub/能力图扫描结果中选择一个适合做成图文和视频的 agent、skill、framework 或 Piko capability。

本轮任务:
- 执行任务:
  - 读取最新 `artifacts/oss_research/*`、`artifacts/capability_map/*`、`artifacts/storytelling/coverage_history.json`，不存在则安全跳过。
  - 优先选择当天新增、可借鉴、与 Piko 自动化目标相关的 skill/agent/framework。
  - 如果当天没有新增 skill，选择一个同类但尚未做过内容的候选。
  - 输出 `artifacts/storytelling/latest_candidate_selection.json`，包含 candidate、reason、evidence_refs、novelty_status、risk_notes。
- 测试任务:
  - 验证 selection JSON 可解析。
  - 验证有 candidate 名称和选择理由。
  - 验证未把未验证能力写成确定结论。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_STORY-1-R01.md`。

允许修改:

- `artifacts/storytelling/*`
- `.piko/summaries/worker_STORY-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要联网抓取新数据；本轮只消费已有扫描结果。
- 不要发布或上传内容。
- 不要把 candidate 直接加入生产能力图。

必须运行的验证:

- Candidate selection JSON parse probe。

完成定义:

- 已选出今日内容主题，或在无新增时选出未覆盖的同类主题。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
