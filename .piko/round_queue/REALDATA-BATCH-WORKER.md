# Piko-worker Task Prompt: REALDATA-1 To REALDATA-6

请一次连续执行 REALDATA-1 到 REALDATA-6，然后停止等待 Piko-verify。

本批次目标：把 Piko 从“单个 approved JSON endpoint 已跑通”推进到“多真实 provider 摘要 endpoint 可受控接入”。必须坚持：没有 provider endpoint 就 blocked；有 provider endpoint 才能 real_collection_performed=true；不得 crawler、scrape、保存全文或伪装全网覆盖。

## 必读文件

`C:\PycharmProjects\Piko\.piko\round_queue\REALDATA-INDEX.md`

## 执行顺序

REALDATA-1-R01 -> REALDATA-1-R02
REALDATA-2-R01 -> REALDATA-2-R02 -> REALDATA-2-R03
REALDATA-3-R01 -> REALDATA-3-R02
REALDATA-4-R01 -> REALDATA-4-R02
REALDATA-5-R01 -> REALDATA-5-R02
REALDATA-6-R01 -> REALDATA-6-R02

## 核心要求

- 复用既有 `packages.collectors.real_market` 和 `packages.discovery.real_market` 的 endpoint-only connector。
- 建立 `packages.realdata` 或等价 pipeline，聚合 Steam / Reddit / SERP / JP / KR approved JSON endpoints。
- 默认不联网。
- 缺 endpoint 时输出 `blocked_for_provider_endpoints`。
- 部分 endpoint 可用时输出 `partial_real_provider_coverage`。
- 多 endpoint 成功时输出 `real_collection_performed=true`，但仍保持 `publish_ready=false` 和 `publishing_performed=false`。
- 最终生成 operator 可读窗口/API，展示每个 provider 的状态、采集数量、过滤结果、内容候选和阻断原因。

## 必须运行的验证

- REALDATA 专项测试
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`
- REALDATA pipeline CLI
- REALDATA API/window probes
- structured guardrail scan

## 状态要求

若至少一个真实 provider endpoint 成功且 pipeline 完整：

```
current_round=REALDATA-1-to-REALDATA-6
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=REALDATA-6-R02
worker_summary_file=.piko/summaries/worker_REALDATA-1-to-REALDATA-6.md
next_round=null
```

若缺少全部 provider endpoint：

```
current_round=REALDATA-1-to-REALDATA-6
worker_status=blocked_for_provider_endpoints
verification_status=not_started
last_completed_round=REALDATA-2-R01
worker_summary_file=.piko/summaries/worker_REALDATA-1-to-REALDATA-6.md
next_round=REALDATA-2-R01
```

## 输出格式

最终 summary 必须包含：

- 修改了什么
- 每个 REALDATA stage 和 round 状态
- 每个 provider endpoint 状态
- real_collection_performed 是否为 true
- partial/full coverage 判断
- 漏斗排行结果
- 内容包结果
- operator surface 结果
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

