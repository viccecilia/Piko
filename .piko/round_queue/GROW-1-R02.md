# Round ID: GROW-1-R02

Round Name: Candidate Normalization And Dedup

本轮目标:

把每日扫描里的项目、skill、agent、framework 候选标准化，并和已有 CAP/OSS/STORY 历史去重。

本轮任务:
- 执行任务:
  - 读取 `latest_scan_intake.json`。
  - 生成 `artifacts/growth_loop/latest_normalized_candidates.json`。
  - 标准字段至少包含 `candidate_id`、`name`、`category`、`github_url`、`stars`、`license`、`piko_relevance`、`risk_level`、`novelty_status`、`dedup_key`。
  - 和 `artifacts/capability_map/latest_capability_map.json`、`artifacts/oss_research/*`、`artifacts/storytelling/*` 做轻量去重。
  - 标记 `new`、`known`、`updated`、`story_only`、`reject_low_fit`。
- 测试任务:
  - 测试重复候选不会重复进入 CAP review。
  - 测试 story_only 不会进入 runtime adoption。
  - 测试 license 高风险候选保留风险标记。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_GROW-1-R02.md`。
  - 生成 `.piko/summaries/worker_GROW-1.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/growth_loop/*`
- `.piko/summaries/worker_GROW-1-R02.md`
- `.piko/summaries/worker_GROW-1.md`
- `.piko/round_status.json`

禁止修改:

- 不要删除历史 artifact 来规避重复。
- 不要自动吸收候选。

必须运行的验证:

- Normalized candidates JSON parse probe。
- Dedup tests。

完成定义:

- 每日扫描候选被标准化、去重，并准备进入 CAP review。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
