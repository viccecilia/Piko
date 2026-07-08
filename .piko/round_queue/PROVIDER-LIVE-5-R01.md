# Round ID: PROVIDER-LIVE-5-R01
Round Name: REALDATA Env Handoff

本轮目标:

生成下一轮 REALDATA 重跑所需 env handoff，让 worker 能验证 partial provider coverage。

本轮任务:
- 执行任务:
  - 生成 `artifacts/provider_live/latest_realdata_env_handoff.json`。
  - 写出 PowerShell env 指令。
  - 明确哪些 provider endpoint 成功，哪些 pending。
- 测试任务:
  - 测试 handoff 包含双 opt-in。
  - 测试 handoff 不包含 secrets。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_PROVIDER-LIVE-5-R01.md`。

允许修改:

- `packages/provider_live/**`
- `tests/**`
- `artifacts/provider_live/**`
- `docs/**`

禁止修改:

- 不得自动写入永久环境变量。
- 不得保存 credentials。

必须运行的验证:

- REALDATA env handoff 专项测试

完成定义:

- 下一轮 REALDATA 如何配置非常清楚。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

