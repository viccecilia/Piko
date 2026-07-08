# Piko-worker Task Prompt: LIVE-CONNECTOR-1 To LIVE-CONNECTOR-5

请一次连续执行 LIVE-CONNECTOR-1 到 LIVE-CONNECTOR-5，然后停止等待 Piko-verify。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\LIVE-CONNECTOR-INDEX.md`

执行顺序：

```text
LIVE-CONNECTOR-1-R01 -> LIVE-CONNECTOR-1-R02
LIVE-CONNECTOR-2-R01 -> LIVE-CONNECTOR-2-R02 -> LIVE-CONNECTOR-2-R03
LIVE-CONNECTOR-3-R01 -> LIVE-CONNECTOR-3-R02
LIVE-CONNECTOR-4-R01 -> LIVE-CONNECTOR-4-R02
LIVE-CONNECTOR-5-R01 -> LIVE-CONNECTOR-5-R02
```

本批次目标：

- 从 connector registry 中选择最低风险 connector：approved_json_endpoint。
- 建立 live connector approval artifact。
- 在显式双 opt-in 和 approved endpoint URL 存在时，执行 bounded live endpoint probe。
- 若 endpoint 缺失，必须 blocked_for_endpoint。
- 若 contract 不通过，必须 failed_contract_validation。
- 若成功，将 live payload normalize 成 signals，并把结果交给 REAL funnel handoff。
- 不发布、不部署、不调用 LLM、不 crawler。

全局禁止项：

- 不启用 Steam/Reddit/JP/KR/SERP live connector。
- 不 crawler。
- 不 scrape HTML。
- 不保存 raw response body、full posts、full pages、full comments。
- 不保存 token/cookie/API key/authorization/credentials。
- 不发布、不上传、不部署、不 commit、不 push。
- 不默认调用 LLM。
- 不绕过 verification，不放宽 Gate。
- 不伪装 live success。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- LIVE-CONNECTOR 专项测试
- Live connector artifacts JSON parse probes
- Endpoint live/blocked probe
- Normalization and REAL handoff probes
- API/window probes if implemented
- Guardrail scan

最终更新 `.piko/round_status.json`：

若完整执行到最终：

```text
current_round=LIVE-CONNECTOR-1-to-LIVE-CONNECTOR-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=LIVE-CONNECTOR-5-R02
worker_summary_file=.piko/summaries/worker_LIVE-CONNECTOR-1-to-LIVE-CONNECTOR-5.md
next_round=null
```

若 endpoint 缺失且无法继续 live：

```text
current_round=LIVE-CONNECTOR-1-to-LIVE-CONNECTOR-5
worker_status=blocked_for_endpoint
verification_status=not_started
last_completed_round=LIVE-CONNECTOR-2-R01
worker_summary_file=.piko/summaries/worker_LIVE-CONNECTOR-1-to-LIVE-CONNECTOR-5.md
next_round=LIVE-CONNECTOR-1-R01
```

最终输出格式：

- 修改了什么
- LIVE-CONNECTOR-1 每个 round 状态
- LIVE-CONNECTOR-2 每个 round 状态
- LIVE-CONNECTOR-3 每个 round 状态
- LIVE-CONNECTOR-4 每个 round 状态
- LIVE-CONNECTOR-5 每个 round 状态
- live connector 状态：success / blocked_for_endpoint / failed_contract_validation / needs_fix
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
