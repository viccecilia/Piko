# Piko-verify Task Prompt: Verify LIVE-1 Approved Live Endpoint Connection

你是 Piko-verify。请验证 Piko-worker 是否完整执行 LIVE-1，而不是验证 REV 或其它队列。

验证范围:

```text
LIVE-1-R01 -> LIVE-1-R02 -> LIVE-1-R03
```

必须检查的 summary:

- `.piko/summaries/worker_LIVE-1-R01.md`
- `.piko/summaries/worker_LIVE-1-R02.md`
- `.piko/summaries/worker_LIVE-1-R03.md`
- `.piko/summaries/worker_LIVE-1.md`

必须运行的验证:

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --fixture`
- `python -m packages.discovery.real_endpoint_verify --fixture --write-artifact`
- `python -m packages.discovery.real_endpoint_verify --live`
- 如果 endpoint env vars 已配置，运行显式 opt-in live verification，并检查 `real_collection_performed=true` 是否真实出现。
- API/window probes for LIVE-1 result surface.

核心验收点:

- LIVE-1-R01:
  - Readiness 能读取并报告 `PIKO_ENABLE_DISCOVERY_REAL_SOURCE`、`PIKO_LIVE_DISCOVERY_TEST`、`PIKO_APPROVED_ENDPOINT_URL`。
  - 默认无 env 时安全 skipped。
  - 双 opt-in 无 URL 时安全 skipped。
  - 非 HTTP/HTTPS 或明显 HTML endpoint 被拒绝/unsupported。
  - readiness output 不泄露 secrets/token/API key。

- LIVE-1-R02:
  - Bounded live endpoint smoke 有 payload size、limit、timeout、snippet length 限制。
  - 无 endpoint 时 skipped 清晰且 `real_collection_performed=false`。
  - 若 endpoint 已配置且 opt-in，必须验证 live response contract、normalized counts、discarded counts、ranking preview、question buckets。
  - live 成功不得保存 raw response body 或完整 source payload。
  - skipped/mock-live 不得伪装成 real-source success。

- LIVE-1-R03:
  - `artifacts/endpoint_verification/latest_endpoint_verification.json` 存在且 JSON 可解析。
  - Artifact 能说明 live passed/skipped/failed。
  - Artifact 包含 mode、real_collection_performed、normalized counts、discarded/unsupported counts、source-level stats、retained fields、safety flags 或 skipped reason。
  - Operator/API surface 能显示 LIVE-1 状态、endpoint 配置状态、热门游戏/问题预览、安全护栏、发布状态未发布。
  - `round_status.json` 进入 ready_for_verify。

安全禁止项扫描:

- 不得发现 crawler。
- 不得发现 HTML scrape 作为默认路径。
- 不得保存 raw response body、raw_text、body、selftext、content、full_comments、raw_page_text、full posts/pages/comments、credentials、secrets、api_key、authorization。
- 不得发布、deploy、commit、push。
- 不得默认调用 LLM、translation API、image generation。
- 不得绕过 verification 或放宽 Gate。
- 不得伪装 skipped/mock-live 为真实采集。
- 不得下载外部图片。

round_status 期望:

- `current_round=LIVE-1`
- `worker_status=ready_for_verify`
- `verification_status=not_started`
- `last_completed_round=LIVE-1-R03`
- `last_verified_round=REV-3-to-REV-6`
- `worker_summary_file=.piko/summaries/worker_LIVE-1.md`
- `next_round=null`

通过后请更新:

- 生成 `.piko/summaries/verify_LIVE-1.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=LIVE-1`
  - `verification_summary_file=.piko/summaries/verify_LIVE-1.md`
  - `next_round=null`
  - UTF-8 no BOM

失败时请更新:

- `worker_status=needs_fix`
- `verification_status=failed`
- `next_round=LIVE-1`
- 写明阻断问题和精确返工任务。

输出格式:

- 验证结论
- 已生成验证报告
- 已运行验证
- Stage 完整性检查
- LIVE-1-R01 检查结果
- LIVE-1-R02 检查结果
- LIVE-1-R03 检查结果
- API / artifact / window 检查
- guardrail 检查
- 发现的问题
- 建议返工任务
