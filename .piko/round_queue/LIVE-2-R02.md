# Round ID: LIVE-2-R02

Round Name: Real Approved Endpoint Live Smoke

本轮目标:

在 R01 preflight ready 后，对真实 approved JSON endpoint 发起一次小流量 live smoke，并证明 `real_collection_performed=true`。

本轮任务:
- 执行任务:
  - 仅在以下条件全部满足时联网：
    - `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
    - `PIKO_LIVE_DISCOVERY_TEST=true`
    - `PIKO_APPROVED_ENDPOINT_URL` 已配置且通过 R01 preflight
  - 发起 bounded request，限制：
    - timeout 有上限
    - payload size 有上限
    - 最多 5 个 games
    - 最多 20 个 questions
    - snippet 长度有上限
  - 验证返回 JSON contract。
  - Normalize 为 `GameHeatSignal` 和 `PlayerQuestionSignal`。
  - 生成 ranking preview 和 question buckets。
  - 写入 `artifacts/endpoint_verification/latest_endpoint_verification.json`，必须包含：
    - `status`
    - `mode=real-source`
    - `real_collection_performed=true`
    - normalized counts
    - discarded/unsupported counts
    - retained fields
    - safety flags
  - 不保存 raw response body 或完整 source payload。
- 测试任务:
  - 成功 live 时 `real_collection_performed=true`。
  - 非 JSON / contract invalid / timeout / payload too large 时安全失败，不进入 ranking success。
  - forbidden fields 被丢弃。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-2-R02.md`。
  - Summary 必须明确真实联网是否发生、normalized games/questions 数量、discarded 数量。

允许修改:

- `packages/discovery/*`
- `packages/collectors/*`
- `artifacts/endpoint_verification/*`
- `tests/test_discovery_search.py`
- `tests/test_live_1.py`
- `.piko/summaries/worker_LIVE-2-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要 crawler 或 scrape HTML。
- 不要保存 raw response body、full source payload、full posts/pages/comments。
- 不要发布、部署、commit、push。
- 不要默认调用 LLM、translation API、image generation。
- 不要把失败/skipped 写成 real-source success。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest tests\test_live_1.py -q`
- `python -m packages.discovery.real_endpoint_verify --live --write-artifact`
- 显式 opt-in live smoke，记录 `real_collection_performed`。

完成定义:

- 若 endpoint 配置正确，真实 live smoke 完成且 `real_collection_performed=true`。
- Artifact 安全且不含 raw/full source。
- 若 endpoint 无效，明确 fail/blocked，不伪装成功。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
