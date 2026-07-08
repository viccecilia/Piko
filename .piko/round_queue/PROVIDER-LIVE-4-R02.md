# Round ID: PROVIDER-LIVE-4-R02
Round Name: Steam Provider Endpoint Validation

本轮目标:

尝试托管或验证 Steam approved JSON endpoint，若成功则输出 REALDATA `PIKO_STEAM_DISCOVERY_URL` handoff。

本轮任务:
- 执行任务:
  - 验证非本地 HTTPS Steam endpoint。
  - 记录 status、host、counts、blocked_reason。
  - 无法托管时保持 deploy-ready。
- 测试任务:
  - 测试 endpoint success / blocked 两种状态。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_PROVIDER-LIVE-4-R02.md` 和 `.piko/summaries/worker_PROVIDER-LIVE-4.md`。

允许修改:

- `packages/provider_live/**`
- `tests/**`
- `artifacts/provider_live/**`

禁止修改:

- 不得把 SERP/Reddit endpoint 当 Steam success。

必须运行的验证:

- Steam endpoint validation probe

完成定义:

- Steam endpoint 状态清楚，可 handoff 或 deploy-ready。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

