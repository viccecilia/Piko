# Piko-worker Task Prompt: EXTERNAL-ENDPOINT-1 To EXTERNAL-ENDPOINT-5

请一次连续执行 EXTERNAL-ENDPOINT-1 到 EXTERNAL-ENDPOINT-5，然后停止等待 Piko-verify。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\EXTERNAL-ENDPOINT-INDEX.md`

执行顺序：

```text
EXTERNAL-ENDPOINT-1-R01 -> EXTERNAL-ENDPOINT-1-R02
EXTERNAL-ENDPOINT-2-R01 -> EXTERNAL-ENDPOINT-2-R02 -> EXTERNAL-ENDPOINT-2-R03
EXTERNAL-ENDPOINT-3-R01 -> EXTERNAL-ENDPOINT-3-R02
EXTERNAL-ENDPOINT-4-R01 -> EXTERNAL-ENDPOINT-4-R02
EXTERNAL-ENDPOINT-5-R01 -> EXTERNAL-ENDPOINT-5-R02
```

本批次目标：

- 从本地 approved endpoint 成功路径推进到外部 approved JSON endpoint。
- 检查外部 endpoint approval、双 opt-in、URL、timeout、payload size。
- 执行 bounded external HTTP probe。
- 成功时生成 external normalized signals，并接回 REAL funnel。
- 产出 internal candidate article package 和 operator result。
- 缺配置或合同失败时正确 blocked/failed，不伪装成功。

全局禁止项：

- 不 crawler。
- 不 scrape HTML。
- 不启用 Steam/Reddit/JP/KR/SERP broad live connector。
- 不保存 raw response body、full posts、full pages、full comments。
- 不保存 token/cookie/API key/authorization/credentials。
- 不发布、不上传、不部署、不 commit、不 push。
- 不默认调用 LLM。
- 不绕过 verification，不放宽 Gate。
- 不声称 broad internet coverage。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- EXTERNAL-ENDPOINT 专项测试
- External endpoint blocked/success probe
- Contract validation probe
- REAL handoff and article candidate probes
- Artifact JSON parse probes
- Guardrail scan

最终更新 `.piko/round_status.json`：

若完整执行：

```text
current_round=EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=EXTERNAL-ENDPOINT-5-R02
worker_summary_file=.piko/summaries/worker_EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5.md
next_round=null
```

若缺外部 endpoint：

```text
current_round=EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5
worker_status=blocked_for_external_endpoint
verification_status=not_started
last_completed_round=EXTERNAL-ENDPOINT-1-R02
worker_summary_file=.piko/summaries/worker_EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5.md
next_round=EXTERNAL-ENDPOINT-1-R01
```

最终输出格式：

- 修改了什么
- EXTERNAL-ENDPOINT-1 每个 round 状态
- EXTERNAL-ENDPOINT-2 每个 round 状态
- EXTERNAL-ENDPOINT-3 每个 round 状态
- EXTERNAL-ENDPOINT-4 每个 round 状态
- EXTERNAL-ENDPOINT-5 每个 round 状态
- external endpoint 状态：success / blocked_for_external_endpoint / failed_contract_validation / needs_fix
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
