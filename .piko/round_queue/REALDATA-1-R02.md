# Round ID: REALDATA-1-R02
Round Name: Provider Approval And Env Policy

本轮目标:

建立真实 provider endpoint 的 approval/env policy，确保只有显式双 opt-in 和 approved endpoint 才能采集。

本轮任务:
- 执行任务:
  - 定义 required env：`PIKO_ENABLE_DISCOVERY_REAL_SOURCE`、`PIKO_LIVE_DISCOVERY_TEST`、各 provider URL。
  - 拒绝 localhost/file/fixture/mock 作为 provider success。
  - 输出 provider readiness artifact。
- 测试任务:
  - 测试缺双 opt-in、缺 endpoint、local URL、fixture URL 均 blocked。
  - 测试合法 HTTPS endpoint 进入 ready 状态。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-1-R02.md` 和 `.piko/summaries/worker_REALDATA-1.md`。

允许修改:

- `packages/realdata/**`
- `packages/shared/config.py`
- `tests/**`
- `artifacts/realdata/**`

禁止修改:

- 不得把 `PIKO_APPROVED_ENDPOINT_URL` 单 endpoint 当作多 provider success。
- 不得让 provider 默认联网。

必须运行的验证:

- REALDATA provider env policy 专项测试

完成定义:

- provider readiness 能准确显示每个 provider 是 ready / missing / rejected / blocked。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

