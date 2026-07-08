# Round ID: GROW-3-R02

Round Name: Verify Task Draft Contract

本轮目标:

为每个 worker task draft 生成对应 verify task draft，让验证标准和实现任务一起产生。

本轮任务:
- 执行任务:
  - 建立 `artifacts/growth_loop/verify_task_draft_contract.json`。
  - verify 草稿字段至少包含 `verify_id`、`source_task_id`、`required_commands`、`artifact_checks`、`guardrail_checks`、`pass_conditions`、`fail_conditions`、`status=draft_only`。
  - verify draft 必须检查不默认联网、不默认 LLM、不自动安装、不自动替换、不发布部署。
- 测试任务:
  - 验证 verify draft contract JSON 可解析。
  - 验证每个 worker draft 都有 verify draft。
  - 验证 guardrail checks 不为空。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_GROW-3-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/growth_loop/*`
- `.piko/summaries/worker_GROW-3-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要自动运行 verify draft。
- 不要降低验证标准。

必须运行的验证:

- Verify task draft contract probe。
- Worker/verify one-to-one tests。

完成定义:

- 每个 worker task 草稿都有对应 verify 草稿。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
