# Round ID: LIVE-2-R01

Round Name: Real Endpoint Intake And Preflight

本轮目标:

读取真实 approved endpoint URL，并在发起联网前完成严格预检。LIVE-2 的目标是真实 live，不是 skipped-live；如果 URL 缺失，本轮必须明确阻塞等待 endpoint。

本轮任务:
- 执行任务:
  - 读取 `PIKO_ENABLE_DISCOVERY_REAL_SOURCE`、`PIKO_LIVE_DISCOVERY_TEST`、`PIKO_APPROVED_ENDPOINT_URL`。
  - 如果 URL 缺失，写清楚 blocked reason，不要继续伪装 live。
  - 对 URL 做 preflight 校验：HTTP/HTTPS、不是本地文件、不是明显 HTML 页面目标、属于 approved endpoint 配置。
  - 确保日志和 summary 不输出 secrets、headers、tokens、API keys。
  - 若 endpoint 需要 API key，必须通过环境变量/安全配置读取，不得写入代码、summary 或 artifact。
- 测试任务:
  - URL 缺失时输出 blocked/skipped reason。
  - 非 HTTP/HTTPS URL 被拒绝。
  - secret-like env 不进入 summary/artifact。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-2-R01.md`。
  - Summary 必须明确：endpoint 是否配置、是否允许进入 R02 真实请求。

允许修改:

- `packages/discovery/*`
- `tests/test_discovery_search.py`
- `tests/test_live_1.py`
- `docs/player_pain_discovery.md`
- `.piko/summaries/worker_LIVE-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要在 URL 缺失时声称 real live passed。
- 不要保存 secret、token、API key、authorization header。
- 不要 crawler、scrape HTML、发布、部署、commit、push。
- 不要默认调用 LLM、translation API、image generation。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest tests\test_live_1.py -q`

完成定义:

- Endpoint preflight 能明确 ready / blocked / unsupported。
- 若 ready，R02 可以发起 bounded live request。
- 若 blocked，必须停止并等待 operator 配置 endpoint。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
