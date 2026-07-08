# Round ID: DOMAIN-2-R03

Round Name: Gaming Domain Eval And Guardrails

本轮目标:

为 gaming domain pack 绑定 eval 和 guardrails，确保抽象后不丢安全边界。

本轮任务:
- 执行任务:
  - 生成 gaming domain eval suite。
  - 覆盖 watchlist/high-risk/publish candidate/source trace/publish disabled。
  - 输出 eval report artifact。
- 测试任务:
  - 测试 high-risk 不进入 publish candidate。
  - 测试 publish_ready=false。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-2-R03.md` 和 `.piko/summaries/worker_DOMAIN-2.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/domain_plugins/*`
- `.piko/summaries/worker_DOMAIN-2-R03.md`
- `.piko/summaries/worker_DOMAIN-2.md`
- `.piko/round_status.json`

禁止修改:

- 不放宽 gaming Gate。

必须运行的验证:

- Gaming domain eval tests

完成定义:

- Gaming domain pack 有自己的 eval 和 guardrails。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
