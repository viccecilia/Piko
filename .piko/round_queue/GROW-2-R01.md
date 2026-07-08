# Round ID: GROW-2-R01

Round Name: CAP Review Decision Rules

本轮目标:

定义每日候选进入 CAP 的判断规则，输出 keep、augment、replace_candidate、deprecate_candidate、reject、story_only、watch。

本轮任务:
- 执行任务:
  - 建立 `artifacts/growth_loop/cap_review_policy.json`。
  - 决策维度至少包含 `fit_to_piko_goal`、`maturity`、`license_safety`、`implementation_cost`、`testability`、`security_risk`、`replacement_value`、`story_value`。
  - 明确 `story_only` 不能进入 runtime queue。
  - 明确 `replace_candidate` 不能自动替换现有能力。
- 测试任务:
  - 测试高风险 license 不会进入 adopt/augment。
  - 测试 story_only 不会进入 worker implementation queue。
  - 测试 replace_candidate 仍需人工批准。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_GROW-2-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/growth_loop/*`
- `.piko/summaries/worker_GROW-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要把任何候选标记为 active capability。
- 不要自动执行替换。

必须运行的验证:

- CAP review policy JSON parse probe。
- Decision policy tests。

完成定义:

- CAP review 有明确、可测试的决策规则。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
