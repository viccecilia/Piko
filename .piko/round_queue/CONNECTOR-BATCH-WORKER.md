# Piko-worker Task Prompt: CONNECTOR-1 To CONNECTOR-5 General Connector Registry

请一次连续执行 CONNECTOR-1 到 CONNECTOR-5，然后停止等待 Piko-verify。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\CONNECTOR-INDEX.md`

执行顺序：

```text
CONNECTOR-1-R01 -> CONNECTOR-1-R02 -> CONNECTOR-1-R03
CONNECTOR-2-R01 -> CONNECTOR-2-R02
CONNECTOR-3-R01 -> CONNECTOR-3-R02 -> CONNECTOR-3-R03
CONNECTOR-4-R01 -> CONNECTOR-4-R02 -> CONNECTOR-4-R03
CONNECTOR-5-R01 -> CONNECTOR-5-R02
```

本批次目标：

- 建立通用 connector registry，不再只依赖单个 approved endpoint。
- 为 gaming 和 ai_tools domain pack 绑定 connector pack。
- 明确 credential / permission / source governance。
- 生成 collection plan dry-run，不默认真实采集。
- 给 operator 一个连接器状态窗口/API，能看到哪些 connector 可用、缺什么配置、是否批准、是否可运行。

重点要求：

- Registry 是 domain-agnostic。
- Connector 默认 candidate/disabled。
- REAL 缺 endpoint 的问题要被 registry 明确表达为 blocked_for_endpoint，而不是伪装成功。
- 所有真实采集仍需 explicit approval + opt-in + endpoint/credential policy。

全局禁止项：

- 不默认联网。
- 不 crawler。
- 不 scrape HTML。
- 不保存 token/cookie/API key/authorization/credentials。
- 不保存 raw/full source。
- 不发布、不上传、不部署、不 commit、不 push。
- 不默认调用 LLM。
- 不绕过 verification，不放宽 Gate。
- 不自动启用 connector。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- CONNECTOR 专项测试
- Connector artifact JSON parse probes
- Credential guardrail probes
- Domain connector routing probes
- Collection dry-run probes
- API/window probes if implemented
- Guardrail scan

最终更新 `.piko/round_status.json`：

```text
current_round=CONNECTOR-1-to-CONNECTOR-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=CONNECTOR-5-R02
worker_summary_file=.piko/summaries/worker_CONNECTOR-1-to-CONNECTOR-5.md
next_round=null
```

最终输出格式：

- 修改了什么
- CONNECTOR-1 每个 round 状态
- CONNECTOR-2 每个 round 状态
- CONNECTOR-3 每个 round 状态
- CONNECTOR-4 每个 round 状态
- CONNECTOR-5 每个 round 状态
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
