# Round ID: REV-2-R01

Round Name: Live Endpoint Opt-In Smoke

本轮目标:

Run a bounded live endpoint smoke only when an approved JSON endpoint URL and explicit opt-in flags are configured.

本轮任务:
- 执行任务:
  - Extend endpoint verification CLI for live smoke with a configured URL.
  - Require explicit flags such as `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true` and `PIKO_LIVE_DISCOVERY_TEST=true`.
  - Bound timeout, payload size, and max records.
  - Return skip when live endpoint URL is absent.
- 测试任务:
  - Default tests skip live smoke.
  - Opt-in without endpoint skips clearly.
  - Mock live endpoint passes with bounded payload.
- 协作验收任务:
  - Worker summary must state whether live smoke was skipped or run and why.

允许修改:

- `packages/discovery/*`
- `tests/test_discovery_search.py`
- `docs/*`
- `.piko/summaries/worker_REV-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- Do not require internet for normal pytest.
- Do not write raw live response body to disk.
- Do not crawl or scrape HTML.

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- Optional only when endpoint is configured: explicit live smoke command.

完成定义:

- Live endpoint smoke is opt-in, bounded, and skipped by default.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
