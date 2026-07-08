# Round ID: LIVE-1-R01

Round Name: Approved Endpoint Configuration Readiness

本轮目标:

确认 Piko 已准备好接入一个 approved JSON endpoint，并在没有 endpoint 时给出清晰 skip/缺项报告，而不是失败或伪装真实采集成功。

本轮任务:
- 执行任务:
  - 检查并完善 approved endpoint configuration/readiness 逻辑。
  - 明确读取并报告：
    - `PIKO_ENABLE_DISCOVERY_REAL_SOURCE`
    - `PIKO_LIVE_DISCOVERY_TEST`
    - `PIKO_APPROVED_ENDPOINT_URL`
  - 若缺少任一 live 条件，输出 `status=skipped`、`real_collection_performed=false`、清晰 skipped reason。
  - 若 URL 存在，先做静态校验：必须是 HTTP/HTTPS JSON endpoint，不接受 HTML page 目标或本地文件路径。
  - 在 docs 中补充如何配置 approved endpoint，以及最小示例 payload。
- 测试任务:
  - 默认无 env 时 live readiness 安全 skipped。
  - 双 opt-in 但无 URL 时安全 skipped。
  - 非 HTTP/HTTPS 或明显 HTML endpoint 被拒绝或 unsupported。
  - readiness output 不包含 secrets/token/API key。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-1-R01.md`。
  - Summary 需说明当前机器是否配置了 approved endpoint URL；如果未配置，要写明下一步需要 operator 提供什么。

允许修改:

- `packages/discovery/*`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`
- `docs/current_state.md`
- `.piko/summaries/worker_LIVE-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要真实联网，除非显式 opt-in 且 URL 已配置。
- 不要 crawler 或 scrape HTML。
- 不要保存 raw response body、完整帖子、完整评论、图片、地图、表格、credentials、secrets。
- 不要发布、部署、commit、push。
- 不要默认调用 LLM、translation API、image generation。
- 不要绕过 verification 或放宽 Gate。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m packages.discovery.real_endpoint_verify --live`

完成定义:

- Live endpoint readiness 能安全判断 ready/skipped/unsupported。
- 缺 endpoint 时不会失败成阻断，也不会伪装成功。
- 配置文档清楚。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
