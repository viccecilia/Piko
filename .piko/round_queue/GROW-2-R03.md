# Round ID: GROW-2-R03

Round Name: Capability Map Feedback Integration

本轮目标:

把 CAP review report 以 proposal-only 方式反馈到 capability map，不改变 active capability。

本轮任务:
- 执行任务:
  - 生成或更新 `artifacts/growth_loop/latest_capability_feedback.json`。
  - 将每日 CAP review 归档为 capability feedback。
  - 对每个候选记录 `target_capability`、`suggested_change`、`status=proposal_only`。
  - 如存在 `/capabilities` API，确保能展示 feedback count 或 latest review summary。
- 测试任务:
  - 验证 feedback JSON 可解析。
  - 验证 `status=proposal_only`。
  - 验证 active capability map 没被自动替换。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_GROW-2-R03.md`。
  - 生成 `.piko/summaries/worker_GROW-2.md`。

允许修改:

- `packages/*`
- `apps/api/routes/*`
- `tests/*`
- `docs/*`
- `artifacts/growth_loop/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_GROW-2-R03.md`
- `.piko/summaries/worker_GROW-2.md`
- `.piko/round_status.json`

禁止修改:

- 不要把 feedback 写成 active adoption。
- 不要自动改 routing policy。

必须运行的验证:

- Feedback JSON parse probe。
- Active capability non-mutation probe。

完成定义:

- CAP 能看到每日 growth feedback，但不会自动吸收。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
