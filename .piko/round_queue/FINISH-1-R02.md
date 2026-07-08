# Round ID: FINISH-1-R02
Round Name: External Live Fetch And Contract Validation

本轮目标:

在显式 opt-in 且 URL 合法时，执行一次 bounded external approved JSON fetch；否则正确停止为 blocked_for_external_endpoint。

本轮任务:
- 执行任务:
  - 实现或复用 final MVP external live fetch pipeline。
  - 限制 timeout、payload size、result count、retained fields。
  - 通过 approved endpoint contract 后才设置 `real_collection_performed=true`。
  - 失败或缺配置时设置 `blocked_for_external_endpoint`，并停止后续真实闭环。
- 测试任务:
  - 测试 live disabled、missing URL、local URL rejected、mock external payload normalized、raw/full fields rejected。
  - 如没有真实 URL，不得伪造 external success。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_FINISH-1-R02.md` 和 `.piko/summaries/worker_FINISH-1.md`。

允许修改:

- `packages/final_mvp/**`
- `packages/external_endpoint/**`
- `tests/**`
- `artifacts/final_mvp/**`
- `.piko/summaries/**`
- `.piko/round_status.json`

禁止修改:

- 不得 crawler 或 scrape HTML。
- 不得保存 raw response body、full posts、full comments。
- 不得继续执行 FINISH-2 到 FINISH-6 的真实成功路径，除非 external contract passed。

必须运行的验证:

- FINISH external live 专项测试
- external endpoint CLI probe
- `python -m pytest`

完成定义:

- 有真实外部 URL 时，输出 external approved endpoint success evidence。
- 无真实外部 URL 时，状态为 blocked_for_external_endpoint，且 final summary 说明缺什么。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

