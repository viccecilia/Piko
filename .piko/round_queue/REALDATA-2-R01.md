# Round ID: REALDATA-2-R01
Round Name: Multi-Provider Connector Orchestrator

本轮目标:

实现多 provider connector orchestrator，统一调用 Steam / Reddit / SERP / JP / KR endpoint-only adapter。

本轮任务:
- 执行任务:
  - 新增 `packages.realdata.pipeline` 或等价模块。
  - 聚合既有 `SteamMarketConnector`、`RedditMarketConnector`、`SERPMarketConnector`、`JPCommunityMarketConnector`、`KRCommunityMarketConnector`。
  - 每个 provider 独立记录 status、endpoint_host、counts、blocked_reason、real_collection_performed。
- 测试任务:
  - mock 多 provider endpoint 成功。
  - mock 部分 provider 成功、部分 blocked。
  - mock endpoint JSON root invalid / HTML invalid。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-2-R01.md`。

允许修改:

- `packages/realdata/**`
- `packages/collectors/**`
- `tests/**`
- `artifacts/realdata/**`

禁止修改:

- 不得直接抓取 Steam/Reddit 页面。
- 不得调用未批准 URL。
- 不得保存完整 response body。

必须运行的验证:

- REALDATA orchestrator 专项测试

完成定义:

- orchestrator 可聚合多个 approved JSON endpoints。
- 缺 endpoint 时不伪造结果。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

