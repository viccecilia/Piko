# Piko-verify Task Prompt: Verify LIVE-2 Real Approved Endpoint Verification

你是 Piko-verify。请只验证 LIVE-2，不要验证 LIVE-1、REV 或其它队列。

LIVE-2 的关键点:

- LIVE-1 是安全 skipped。
- LIVE-2 必须证明真实 approved endpoint 是否已经配置并联网。
- 只有出现真实 `real_collection_performed=true`，才能把 LIVE-2 标为 real-live passed。
- 如果 endpoint 缺失，结论应是 blocked_for_endpoint 或 failed/missing_endpoint，不应标为真实通过。

验证范围:

```text
LIVE-2-R01 -> LIVE-2-R02 -> LIVE-2-R03
```

必须检查的 summary:

- `.piko/summaries/worker_LIVE-2-R01.md`
- `.piko/summaries/worker_LIVE-2-R02.md`
- `.piko/summaries/worker_LIVE-2-R03.md`
- `.piko/summaries/worker_LIVE-2.md`

必须运行的验证:

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest tests\test_live_1.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --live --write-artifact`
- API/window probes for LIVE-2 result surface.

核心验收点:

- LIVE-2-R01:
  - Endpoint URL 配置状态清晰。
  - 如果缺 `PIKO_APPROVED_ENDPOINT_URL`，worker 必须报告 blocked，不得继续伪装成功。
  - URL preflight 拒绝非 HTTP/HTTPS、HTML endpoint、本地文件路径。
  - 不泄露 secret/token/API key/header。

- LIVE-2-R02:
  - 如果 endpoint 已配置并 opt-in，必须发生真实 live request。
  - Contract validation 通过。
  - Artifact 显示 `mode=real-source`。
  - Artifact 显示 `real_collection_performed=true`。
  - Normalized game/question counts 或 live-empty reason 清晰。
  - 不保存 raw response body、完整 source payload、full posts/pages/comments。
  - 如果 endpoint 失败，必须显示 failed/blocked，不得显示 success。

- LIVE-2-R03:
  - Operator/API surface 显示 LIVE-2 状态。
  - 显示 live_endpoint_status、mode、real_collection_performed、normalized counts、top games/questions preview、artifact path。
  - publishing_performed=false。
  - 不得把 blocked/skipped 显示成 live success。

安全禁止项扫描:

- 不得发现 crawler。
- 不得发现 HTML scrape 作为默认路径。
- 不得保存 raw response body、raw_text、body、selftext、content、full_comments、raw_page_text、full posts/pages/comments、credentials、secrets、api_key、authorization。
- 不得发布、deploy、commit、push。
- 不得默认调用 LLM、translation API、image generation。
- 不得绕过 verification 或放宽 Gate。
- 不得下载外部图片。

通过条件:

真实 live pass 需要:

- `worker_status=ready_for_verify`
- artifact `status=passed`
- artifact `mode=real-source`
- artifact `real_collection_performed=true`
- no raw/full source retention

如果 endpoint 缺失:

- 不要标为 passed。
- 允许结论为 `blocked_for_endpoint`。
- 更新 `round_status.json`：
  - `worker_status=blocked_for_endpoint`
  - `verification_status=failed` 或 `blocked`
  - `next_round=LIVE-2-R01`
  - 明确要求配置 `PIKO_APPROVED_ENDPOINT_URL`

通过后请更新:

- 生成 `.piko/summaries/verify_LIVE-2.md`
- 更新 `.piko/round_status.json`：
  - `current_round=LIVE-2`
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=LIVE-2`
  - `verification_summary_file=.piko/summaries/verify_LIVE-2.md`
  - `next_round=null`
  - UTF-8 no BOM

输出格式:

- 验证结论
- 是否真实联网
- `real_collection_performed` 值
- 已生成验证报告
- 已运行验证
- Stage 完整性检查
- LIVE-2-R01 检查结果
- LIVE-2-R02 检查结果
- LIVE-2-R03 检查结果
- API / artifact / window 检查
- guardrail 检查
- 发现的问题
- 建议返工任务
