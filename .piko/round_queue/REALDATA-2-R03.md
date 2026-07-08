# Round ID: REALDATA-2-R03
Round Name: Provider Guardrail And Failure Modes

本轮目标:

强化 provider failure modes，确保 provider 失败不会导致伪成功或安全边界破裂。

本轮任务:
- 执行任务:
  - 处理 timeout、invalid JSON、HTML response、oversized payload、missing required fields。
  - 每个 provider 失败记录 `failed_contract_validation` 或 `blocked_for_provider_endpoint`。
  - 写入安全摘要。
- 测试任务:
  - 覆盖 HTML response rejected。
  - 覆盖 forbidden field stripped/rejected。
  - 覆盖 oversized payload blocked。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-2-R03.md` 和 `.piko/summaries/worker_REALDATA-2.md`。

允许修改:

- `packages/realdata/**`
- `packages/collectors/**`
- `tests/**`
- `artifacts/realdata/**`

禁止修改:

- 不得吞掉错误后标记 success。
- 不得把 provider failure 当作空成功。

必须运行的验证:

- REALDATA failure mode 专项测试

完成定义:

- provider 失败可解释、可追踪、不可伪成功。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

