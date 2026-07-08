# Piko-worker Task Prompt: PROVIDER-LIVE-1 To PROVIDER-LIVE-5

请一次连续执行 PROVIDER-LIVE-1 到 PROVIDER-LIVE-5，然后停止等待 Piko-verify。

## 背景

REALDATA-1 到 REALDATA-6 已通过，但属于“正确安全阻断”：没有配置 Steam / Reddit / SERP / JP / KR provider endpoint，所以停在 `blocked_for_provider_endpoints`。本批次目标是先做最小真实 provider 覆盖，优先 SERP，其次 Reddit，再 Steam，让 REALDATA 下一轮可以达到 `partial_real_provider_coverage`。

## 必读文件

`C:\PycharmProjects\Piko\.piko\round_queue\PROVIDER-LIVE-INDEX.md`

## 执行顺序

PROVIDER-LIVE-1-R01 -> PROVIDER-LIVE-1-R02
PROVIDER-LIVE-2-R01 -> PROVIDER-LIVE-2-R02
PROVIDER-LIVE-3-R01 -> PROVIDER-LIVE-3-R02
PROVIDER-LIVE-4-R01 -> PROVIDER-LIVE-4-R02
PROVIDER-LIVE-5-R01 -> PROVIDER-LIVE-5-R02

## 核心目标

- 生成 SERP / Reddit / Steam 三个 provider approved JSON package。
- 至少尝试托管或验证一个非本地 HTTPS provider endpoint。
- 输出 REALDATA 重跑所需 env handoff：
  - `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
  - `PIKO_LIVE_DISCOVERY_TEST=true`
  - `PIKO_SERP_DISCOVERY_URL=<approved provider endpoint>`
  - 可选 `PIKO_REDDIT_DISCOVERY_URL=<approved provider endpoint>`
  - 可选 `PIKO_STEAM_DISCOVERY_URL=<approved provider endpoint>`
- 如果至少一个 provider endpoint 验证成功，标记 `provider_live_status=partial_provider_endpoint_ready`。
- 如果无法托管或验证任何外部 endpoint，标记 `deploy_ready_pending_provider_host`，不得伪装成功。

## 禁止

- 不 crawler。
- 不 scrape HTML。
- 不直接抓 Steam/Reddit/SERP 网页。
- 不保存 raw/full source。
- 不保存 token/cookie/API key/authorization/credentials/secrets。
- 不发布、不上传、不部署、不 commit、不 push。
- 不默认 LLM。
- 不把单 provider partial coverage 说成 broad internet coverage。

## 必须运行的验证

- PROVIDER-LIVE 专项测试，如不存在则新增并运行。
- `python -m pytest tests\test_realdata_pipeline.py -q`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- provider package JSON parse probes。
- provider endpoint validation probe。
- structured guardrail scan。

## 状态要求

如果至少一个 provider endpoint 成功：

```
current_round=PROVIDER-LIVE-1-to-PROVIDER-LIVE-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=PROVIDER-LIVE-5-R02
worker_summary_file=.piko/summaries/worker_PROVIDER-LIVE-1-to-PROVIDER-LIVE-5.md
next_round=null
```

如果没有任何外部 provider endpoint 成功，但 package 已准备好：

```
current_round=PROVIDER-LIVE-1-to-PROVIDER-LIVE-5
worker_status=deploy_ready_pending_provider_host
verification_status=not_started
last_completed_round=PROVIDER-LIVE-5-R02
worker_summary_file=.piko/summaries/worker_PROVIDER-LIVE-1-to-PROVIDER-LIVE-5.md
next_round=PROVIDER-LIVE-2-R02
```

## 输出格式

最终 summary 必须包含：

- 修改了什么
- 每个 PROVIDER-LIVE stage / round 状态
- SERP endpoint 状态
- Reddit endpoint 状态
- Steam endpoint 状态
- 是否有 partial provider endpoint ready
- REALDATA env handoff
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

