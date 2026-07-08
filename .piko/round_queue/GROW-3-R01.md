# Round ID: GROW-3-R01

Round Name: Worker Task Draft Contract

本轮目标:

定义从 CAP review 生成 worker task 草稿的合同。草稿只供人工确认，不自动执行。

本轮任务:
- 执行任务:
  - 建立 `artifacts/growth_loop/worker_task_draft_contract.json`。
  - 草稿字段至少包含 `task_id`、`source_candidate_id`、`round_name`、`goal`、`tasks`、`allowed_changes`、`forbidden_changes`、`required_validation`、`definition_of_done`、`status=draft_only`。
  - 明确只有 `next_action=draft_worker_task` 的候选可生成 worker task draft。
- 测试任务:
  - 验证 contract JSON 可解析。
  - 验证 story_only/watch/reject 不生成 worker task。
  - 验证所有草稿包含禁止项。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_GROW-3-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/growth_loop/*`
- `.piko/summaries/worker_GROW-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要把草稿写入 active round queue。
- 不要自动执行 worker task。

必须运行的验证:

- Worker task draft contract probe。
- Draft-only tests。

完成定义:

- Worker task 草稿合同明确，并保持 draft-only。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
