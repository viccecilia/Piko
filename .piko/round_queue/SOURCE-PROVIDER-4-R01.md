# Round ID: SOURCE-PROVIDER-4-R01

Round Name: Piko External Endpoint Env Handoff

本轮目标:

生成后续 EXTERNAL-ENDPOINT 重跑所需的 env/config 指令。

本轮任务:
- 执行任务:
  - 生成 Piko env handoff artifact。
  - 包含 PowerShell 指令：
    - `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
    - `PIKO_LIVE_DISCOVERY_TEST=true`
    - `PIKO_APPROVED_ENDPOINT_URL=<external approved json url>`
  - 若无外部 URL，给出待替换占位符和部署步骤。
- 测试任务:
  - 测试 handoff 不含 secrets。
  - 测试 no external URL 时不能标记 ready_to_run_external=true。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SOURCE-PROVIDER-4-R01.md`。

允许修改:

- `docs/*`
- `tests/*`
- `artifacts/source_provider/*`
- `.piko/summaries/worker_SOURCE-PROVIDER-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不直接设置全局环境变量。

必须运行的验证:

- Env handoff tests

完成定义:

- 后续 EXTERNAL-ENDPOINT 如何重跑很清楚。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
