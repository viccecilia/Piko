# Round ID: PROVIDER-LIVE-2-R02
Round Name: SERP Provider Endpoint Validation

本轮目标:

尝试托管或验证 SERP approved JSON endpoint，若成功则输出 REALDATA `PIKO_SERP_DISCOVERY_URL` handoff。

本轮任务:
- 执行任务:
  - 如果可行，生成/验证非本地 HTTPS SERP endpoint。
  - 若无法托管，输出 `deploy_ready_pending_provider_host`。
  - 更新 `latest_provider_endpoint_status.json`。
- 测试任务:
  - 测试成功 endpoint JSON contract。
  - 测试缺 endpoint 不伪装成功。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_PROVIDER-LIVE-2-R02.md` 和 `.piko/summaries/worker_PROVIDER-LIVE-2.md`。

允许修改:

- `packages/provider_live/**`
- `tests/**`
- `artifacts/provider_live/**`

禁止修改:

- 不得上传凭据。
- 不得使用需要登录的私有 URL。

必须运行的验证:

- SERP endpoint validation probe

完成定义:

- 有 SERP endpoint 时可被 REALDATA 使用；无 endpoint 时状态诚实。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

