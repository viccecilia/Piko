# Round ID: LIVE-1-R02

Round Name: Bounded Live Endpoint Smoke

本轮目标:

在 approved endpoint URL 已配置且显式 opt-in 的情况下，执行一次小流量真实联网 smoke；如果未配置，则保持安全 skipped，并完整验证 skip 行为。

本轮任务:
- 执行任务:
  - 调用 approved JSON endpoint，限制：
    - 最多 5 个 games
    - 最多 20 个 questions
    - timeout 有上限
    - payload size 有上限
    - snippet length 有上限
  - 对 live payload 运行 approved contract validation。
  - Normalize 成 `GameHeatSignal` / `PlayerQuestionSignal`。
  - 生成 endpoint verification result：normalized counts、discarded counts、ranking preview、question buckets、mode、real_collection_performed。
  - 不保存 raw live response body 或完整 source payload。
  - 如果请求失败、超时、非 JSON、contract 不通过，输出安全 fail/skip，不继续进入候选文章。
- 测试任务:
  - 默认测试不触网。
  - mock-live / fixture 仍通过。
  - live 成功时必须 `real_collection_performed=true`。
  - live skipped 时必须 `real_collection_performed=false` 且 reason 清晰。
  - forbidden fields 被丢弃。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-1-R02.md`。
  - Summary 需明确：本机是否真的联网、endpoint URL 是否配置、结果是 passed/skipped/failed。

允许修改:

- `packages/discovery/*`
- `packages/collectors/*`
- `tests/test_discovery_search.py`
- `artifacts/endpoint_verification/*`
- `docs/player_pain_discovery.md`
- `.piko/summaries/worker_LIVE-1-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要 crawler。
- 不要 scrape HTML。
- 不要保存 raw response body、full posts、full comments、raw payload dumps。
- 不要发布、部署、commit、push。
- 不要默认调用 LLM、translation API、image generation。
- 不要绕过 verification 或放宽 Gate。
- 不要伪装 skipped/fallback 为真实 live success。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m packages.discovery.real_endpoint_verify --fixture`
- `python -m packages.discovery.real_endpoint_verify --fixture --write-artifact`
- `python -m packages.discovery.real_endpoint_verify --live`
- 如果 env 已配置，运行显式 opt-in live smoke，并记录结果。

完成定义:

- 有 approved endpoint 时，小流量 live smoke 可安全执行并产出 bounded artifact。
- 无 endpoint 时，skip 行为清楚且测试通过。
- 无 raw/full source 保留。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
