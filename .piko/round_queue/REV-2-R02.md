# Round ID: REV-2-R02

Round Name: Live Normalization And Ranking Probe

本轮目标:

Prove approved endpoint data can normalize and enter hot game/question rankings.

本轮任务:
- 执行任务:
  - Feed live or mock-live approved endpoint data into the same normalizer used by RM.
  - Produce ranking preview with mode `real-source` when live data is actually used, otherwise `mock-live`.
  - Include Top hot games and question buckets.
  - Preserve `real_collection_performed` accurately.
- 测试任务:
  - Mock-live endpoint data produces expected rankings.
  - Default fixture path still reports `real_collection_performed=false`.
  - Live mode cannot claim success when skipped.
- 协作验收任务:
  - Worker summary must include ranking preview and whether source was live or mock-live.

允许修改:

- `packages/discovery/*`
- `tests/test_discovery_search.py`
- `.piko/summaries/worker_REV-2-R02.md`
- `.piko/round_status.json`

禁止修改:

- Do not mix skipped live data with real-source success.
- Do not save raw/full source.
- Do not publish rankings externally.

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m packages.discovery.real_endpoint_verify --fixture`

完成定义:

- Endpoint data can flow into rankings, and mode/real_collection flags are truthful.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
