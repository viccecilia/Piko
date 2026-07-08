# Piko-verify Task Prompt: Verify PROVIDER-LIVE-1 To PROVIDER-LIVE-5

请一次性验证 PROVIDER-LIVE-1 到 PROVIDER-LIVE-5 连续批次，不要只验单个 round。

## 验证入口

`C:\PycharmProjects\Piko\.piko\summaries\worker_PROVIDER-LIVE-1-to-PROVIDER-LIVE-5.md`

## 背景

REALDATA 已通过为“正确安全阻断”，原因是没有 provider endpoints。本批次应准备 SERP / Reddit / Steam provider approved JSON package，并尽可能验证至少一个非本地 HTTPS provider endpoint，为下一轮 REALDATA partial coverage 做准备。

## 必验内容

- 所有 PROVIDER-LIVE round summary 存在。
- 所有 stage summary 存在。
- final summary 存在。
- provider packages 可解析，并符合 REALDATA provider contract。
- localhost / file / fixture / mock 不得标记为 provider success。
- 如果外部 endpoint 成功，必须证明 endpoint 是非本地 HTTPS 且返回 approved JSON。
- 如果没有外部 endpoint 成功，必须是 `deploy_ready_pending_provider_host`，不得伪装 partial coverage。

## 必验命令

- PROVIDER-LIVE 专项测试
- `python -m pytest tests\test_realdata_pipeline.py -q`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- provider package JSON parse probes
- provider endpoint validation probe
- structured guardrail scan

## Guardrail 必查

- 无 crawler。
- 无 HTML scrape。
- 无 direct Steam/Reddit/SERP scraping。
- 无 raw/full source 保存。
- 无 token/cookie/API key/authorization/credentials/secrets 保存。
- 无发布、上传、部署、commit、push。
- 无默认 LLM。
- 无 broad internet coverage 夸大。
- 不把单 provider success 当成 full provider coverage。

## 通过条件

如果至少一个 provider endpoint 成功：

- `provider_live_status=partial_provider_endpoint_ready`
- 至少一个 provider 的 `real_collection_performed=true`
- coverage 必须是 partial。
- 输出 REALDATA env handoff。
- 不发布、不上传、不部署。

如果没有 provider endpoint 成功：

- `provider_live_status=deploy_ready_pending_provider_host` 或等价状态。
- provider package 已生成。
- REALDATA env handoff 清楚。
- 不伪装 provider live success。

## 验收输出

生成 `.piko/summaries/verify_PROVIDER-LIVE-1-to-PROVIDER-LIVE-5.md`。

通过时更新：

```
worker_status=complete
verification_status=passed
last_verified_round=PROVIDER-LIVE-1-to-PROVIDER-LIVE-5
verification_summary_file=.piko/summaries/verify_PROVIDER-LIVE-1-to-PROVIDER-LIVE-5.md
next_round=null
```

失败时更新：

```
worker_status=needs_fix
verification_status=failed
next_round=PROVIDER-LIVE-1-to-PROVIDER-LIVE-5
```

