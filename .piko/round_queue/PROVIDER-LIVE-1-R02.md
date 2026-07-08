# Round ID: PROVIDER-LIVE-1-R02
Round Name: Provider Hosting Policy

本轮目标:

定义 provider endpoint 托管/验证策略，明确什么算 provider live success。

本轮任务:
- 执行任务:
  - 拒绝 localhost、127.0.0.1、file、fixture、mock。
  - 只接受非本地 HTTP(S) approved JSON endpoint。
  - 定义 endpoint validation artifact。
- 测试任务:
  - 测试 local/file/fixture/mock 被拒绝。
  - 测试合法 HTTPS JSON 可进入 ready。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_PROVIDER-LIVE-1-R02.md` 和 `.piko/summaries/worker_PROVIDER-LIVE-1.md`。

允许修改:

- `packages/provider_live/**`
- `tests/**`
- `artifacts/provider_live/**`

禁止修改:

- 不得把 FINISH 的 `PIKO_APPROVED_ENDPOINT_URL` 单 endpoint 当 provider endpoint。

必须运行的验证:

- PROVIDER-LIVE hosting policy 专项测试

完成定义:

- provider live success 定义可验证、不可混淆。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

