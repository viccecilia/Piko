# Piko-verify Task Prompt: Verify EXTERNAL-ENDPOINT-1 To EXTERNAL-ENDPOINT-5

请一次性验证 EXTERNAL-ENDPOINT-1 到 EXTERNAL-ENDPOINT-5 连续批次。通过条件取决于环境：如果没有外部 approved endpoint，正确 blocked_for_external_endpoint 是安全通过；如果配置完整，必须验证 bounded external live collection 和 REAL handoff evidence。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5.md`

验证范围：

```text
EXTERNAL-ENDPOINT-1-R01 -> EXTERNAL-ENDPOINT-1-R02
EXTERNAL-ENDPOINT-2-R01 -> EXTERNAL-ENDPOINT-2-R02 -> EXTERNAL-ENDPOINT-2-R03
EXTERNAL-ENDPOINT-3-R01 -> EXTERNAL-ENDPOINT-3-R02
EXTERNAL-ENDPOINT-4-R01 -> EXTERNAL-ENDPOINT-4-R02
EXTERNAL-ENDPOINT-5-R01 -> EXTERNAL-ENDPOINT-5-R02
```

必须检查：

- 所有已执行 EXTERNAL-ENDPOINT round summary 存在。
- 所有已执行 EXTERNAL-ENDPOINT stage summary 存在。
- final summary `.piko/summaries/worker_EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- 缺 endpoint 时可以是 `blocked_for_external_endpoint`。
- 完整成功时应为 `ready_for_verify`。

必须检查 artifacts：

- External endpoint approval artifact
- External endpoint readiness artifact
- Bounded HTTP probe artifact
- Contract validation artifact
- External normalized signals artifact
- REAL funnel handoff artifact
- Internal article candidate artifact
- Operator external endpoint result artifact

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- EXTERNAL-ENDPOINT专项测试
- External endpoint blocked/success probe
- Contract validation probe
- REAL handoff and article candidate probes
- API/window probes if implemented
- Guardrail scan

核心验收点：

- external endpoint success 必须有 `real_collection_performed=true` evidence。
- success scope 必须是 `external_approved_endpoint`。
- 不得声称 broad internet coverage。
- 缺 URL/opt-in 时必须 blocked，不得回退 fixture 冒充 external。
- 不保存 raw response body、full posts、full comments、secrets。
- REAL handoff / article handoff 仍是 candidate/internal，publish_ready=false，publishing_performed=false。

安全禁止项：

- 不得 crawler 或 scrape HTML。
- 不得发布、上传、部署、commit、push。
- 不得默认调用 LLM。
- 不得保存 raw/full source、secrets、credentials、token、cookie、API key、authorization。
- 不得绕过 verification 或放宽 Gate。

通过时：

- 生成 `.piko/summaries/verify_EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete` 或保留安全 blocked 状态并写明原因
  - `verification_status=passed`
  - `last_verified_round=EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5`
  - `verification_summary_file=.piko/summaries/verify_EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5`

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- EXTERNAL-ENDPOINT-1 检查结果
- EXTERNAL-ENDPOINT-2 检查结果
- EXTERNAL-ENDPOINT-3 检查结果
- EXTERNAL-ENDPOINT-4 检查结果
- EXTERNAL-ENDPOINT-5 检查结果
- external endpoint success/blocked 状态
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
