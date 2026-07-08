# Piko-verify Task Prompt: Verify LIVE-CONNECTOR-1 To LIVE-CONNECTOR-5

请一次性验证 LIVE-CONNECTOR-1 到 LIVE-CONNECTOR-5 连续批次。通过条件取决于环境：如果缺 endpoint，正确 blocked_for_endpoint 是安全通过；如果配置完整，必须验证 bounded live collection 和 REAL handoff evidence。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_LIVE-CONNECTOR-1-to-LIVE-CONNECTOR-5.md`

验证范围：

```text
LIVE-CONNECTOR-1-R01 -> LIVE-CONNECTOR-1-R02
LIVE-CONNECTOR-2-R01 -> LIVE-CONNECTOR-2-R02 -> LIVE-CONNECTOR-2-R03
LIVE-CONNECTOR-3-R01 -> LIVE-CONNECTOR-3-R02
LIVE-CONNECTOR-4-R01 -> LIVE-CONNECTOR-4-R02
LIVE-CONNECTOR-5-R01 -> LIVE-CONNECTOR-5-R02
```

必须检查：

- 所有已执行 LIVE-CONNECTOR round summary 存在。
- 所有已执行 LIVE-CONNECTOR stage summary 存在。
- final summary `.piko/summaries/worker_LIVE-CONNECTOR-1-to-LIVE-CONNECTOR-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- 如果 endpoint 缺失，状态可以是 `blocked_for_endpoint`。
- 如果 endpoint 完整并全批次完成，状态应为 `ready_for_verify`。

必须检查 artifacts：

- Live connector selection artifact
- Live connector approval artifact
- Endpoint readiness artifact
- Endpoint verification result artifact
- Bounded live collection artifact
- Normalized signals artifact
- Connector registry feedback artifact
- REAL funnel handoff artifact
- Operator live connector surface artifact

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- LIVE-CONNECTOR专项测试
- Live connector artifact JSON parse probes
- Endpoint live/blocked probe
- Normalization and REAL handoff probes
- API/window probes if implemented
- Guardrail scan

核心验收点：

- 只能选择 `approved_json_endpoint` 作为 live connector。
- 缺双 opt-in 或 endpoint URL 时必须 blocked_for_endpoint。
- live 成功时必须有 real_collection_performed=true 和 endpoint verification evidence。
- 无论成功或 blocked，都不得保存 raw response body、full posts、full comments、secrets。
- REAL handoff 只产生 candidate/internal output，不发布。
- Steam/Reddit/JP/KR/SERP live connector 没有被启用。

安全禁止项：

- 不得 crawler 或 scrape HTML。
- 不得发布、上传、部署、commit、push。
- 不得默认调用 LLM。
- 不得保存 raw/full source、secrets、credentials、token、cookie、API key、authorization。
- 不得绕过 verification 或放宽 Gate。

通过时：

- 生成 `.piko/summaries/verify_LIVE-CONNECTOR-1-to-LIVE-CONNECTOR-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete` 或保留安全 blocked 状态并写明原因
  - `verification_status=passed`
  - `last_verified_round=LIVE-CONNECTOR-1-to-LIVE-CONNECTOR-5`
  - `verification_summary_file=.piko/summaries/verify_LIVE-CONNECTOR-1-to-LIVE-CONNECTOR-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=LIVE-CONNECTOR-1-to-LIVE-CONNECTOR-5`

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- LIVE-CONNECTOR-1 检查结果
- LIVE-CONNECTOR-2 检查结果
- LIVE-CONNECTOR-3 检查结果
- LIVE-CONNECTOR-4 检查结果
- LIVE-CONNECTOR-5 检查结果
- live connector success/blocked 状态
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
