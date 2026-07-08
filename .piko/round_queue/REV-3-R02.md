# Round ID: REV-3-R02

Round Name: Real Search Endpoint Adapter

本轮目标:

实现受控真实搜索 endpoint adapter，让 Piko 可以通过 approved JSON endpoint 获取“热门游戏”和“玩家问题”摘要信号，但默认不触网。

本轮任务:
- 执行任务:
  - 新增或扩展 real search adapter，输入 query/source/limit/timeout，输出 `GameHeatSignal` 和 `PlayerQuestionSignal`。
  - 支持 mock-live payload，明确 `mode=mock-live` 且 `real_collection_performed=false`。
  - 支持 opt-in live mode，只有在双开关和 approved URL 存在时才请求 endpoint。
  - 限制响应大小、结果数量、snippet 长度和 retained fields。
  - 记录 discarded/unsupported record counts，但不要保存原始 payload dump。
- 测试任务:
  - mock-live Steam / Reddit / SERP / JP / KR payload 可以 normalize。
  - 默认 live 调用安全 skipped。
  - opt-in 无 URL 安全 skipped。
  - forbidden fields 不会进入 normalized output。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-3-R02.md`。
  - Summary 需说明 adapter 输入、输出、skip 条件、discard 统计。

允许修改:

- `packages/discovery/*`
- `packages/collectors/*`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`
- `.piko/summaries/worker_REV-3-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要默认触网。
- 不要 crawler 或 scrape HTML。
- 不要保存 raw response body、完整帖子、完整评论或完整网页。
- 不要发布、部署、commit、push。
- 不要默认调用 LLM 或 translation API。
- 不要绕过 verification 或放宽 Gate。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m packages.discovery.real_endpoint_verify --fixture`
- `python -m packages.discovery.real_endpoint_verify --live`

完成定义:

- Adapter 能从 mock-live/fixture 产出 normalized game/question signals。
- Live path 受 opt-in 和 approved endpoint 保护。
- 安全字段和 discarded counts 可被验证。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
