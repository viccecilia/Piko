# Round ID: SOURCE-PROVIDER-1-R01

Round Name: Provider Strategy Selection

本轮目标:

选择外部 approved JSON endpoint provider 策略，明确最快可行路径和备选路径。

本轮任务:
- 执行任务:
  - 生成 provider strategy artifact。
  - 比较 GitHub Raw/Gist、Cloudflare Pages、Vercel/Netlify、user-owned API。
  - 选择默认策略：static JSON provider package first。
- 测试任务:
  - 测试 strategy artifact 可解析。
  - 测试 localhost/file/fixture 不在 external provider 列表。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SOURCE-PROVIDER-1-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/source_provider/*`
- `.piko/summaries/worker_SOURCE-PROVIDER-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不部署远程。
- 不保存凭据。

必须运行的验证:

- Provider strategy tests

完成定义:

- 外部 endpoint 来源策略清楚，且不把本地地址算作 external。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
