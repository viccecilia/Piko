# Round ID: GROW-4-R01

Round Name: Growth Operator API

本轮目标:

提供只读 API，让操作员查看每日 growth 状态、CAP review、draft queue package。

本轮任务:
- 执行任务:
  - 新增或更新只读 endpoint，例如 `/growth/status`。
  - 输出必须包含 `candidate_only=true`、`publish_ready=false`、`auto_apply_performed=false`、`human_approval_required=true`。
  - API 不得触发扫描、安装、执行、发布。
- 测试任务:
  - API probe 返回 200。
  - 安全字段正确。
  - unknown/missing artifacts 时安全降级。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_GROW-4-R01.md`。

允许修改:

- `apps/api/routes/*`
- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/growth_loop/*`
- `.piko/summaries/worker_GROW-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要让 API 执行 worker task。
- 不要让 API 调用外网或 LLM。

必须运行的验证:

- `/growth/status` API probe if implemented。
- API safety tests。

完成定义:

- 操作员可以通过 API 查看 growth loop 状态。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
