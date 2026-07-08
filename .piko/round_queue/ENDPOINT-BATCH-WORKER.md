# Piko-worker Task Prompt: ENDPOINT-1 To ENDPOINT-5 Local Approved Endpoint Success Path

请一次连续执行 ENDPOINT-1 到 ENDPOINT-5，然后停止等待 Piko-verify。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\ENDPOINT-INDEX.md`

执行顺序：

```text
ENDPOINT-1-R01 -> ENDPOINT-1-R02
ENDPOINT-2-R01 -> ENDPOINT-2-R02 -> ENDPOINT-2-R03
ENDPOINT-3-R01 -> ENDPOINT-3-R02
ENDPOINT-4-R01 -> ENDPOINT-4-R02
ENDPOINT-5-R01 -> ENDPOINT-5-R02
```

本批次目标：

- 把现有 approved endpoint fixture 提升为本地可控 HTTP JSON endpoint。
- 用测试/CLI 显式设置双 opt-in 和 local endpoint URL。
- 跑通 approved_json_endpoint live connector success path。
- 生成 normalized live signals。
- 接回 REAL funnel，生成 Top candidates / pain buckets / internal article handoff。
- 明确这只是 local approved endpoint success，不是全网真实覆盖。

全局禁止项：

- 不 crawler。
- 不 scrape HTML。
- 不启用 Steam/Reddit/JP/KR/SERP live connector。
- 不保存 raw response body、full posts、full pages、full comments。
- 不保存 token/cookie/API key/authorization/credentials。
- 不发布、不上传、不部署、不 commit、不 push。
- 不默认调用 LLM。
- 不绕过 verification，不放宽 Gate。
- 不声称 broad internet coverage。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- ENDPOINT 专项测试
- Local endpoint smoke
- Live connector success path probe
- REAL handoff success probe
- Artifact JSON parse probes
- Guardrail scan

最终更新 `.piko/round_status.json`：

```text
current_round=ENDPOINT-1-to-ENDPOINT-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=ENDPOINT-5-R02
worker_summary_file=.piko/summaries/worker_ENDPOINT-1-to-ENDPOINT-5.md
next_round=null
```

最终输出格式：

- 修改了什么
- ENDPOINT-1 每个 round 状态
- ENDPOINT-2 每个 round 状态
- ENDPOINT-3 每个 round 状态
- ENDPOINT-4 每个 round 状态
- ENDPOINT-5 每个 round 状态
- local endpoint / live connector 状态
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
