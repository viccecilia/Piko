# Piko-verify Task Prompt: Verify ENDPOINT-1 To ENDPOINT-5

请一次性验证 ENDPOINT-1 到 ENDPOINT-5 连续批次。重点确认 Piko 是否通过本地可控 approved JSON endpoint 跑通 live connector success path，并且没有声称全网真实覆盖。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_ENDPOINT-1-to-ENDPOINT-5.md`

验证范围：

```text
ENDPOINT-1-R01 -> ENDPOINT-1-R02
ENDPOINT-2-R01 -> ENDPOINT-2-R02 -> ENDPOINT-2-R03
ENDPOINT-3-R01 -> ENDPOINT-3-R02
ENDPOINT-4-R01 -> ENDPOINT-4-R02
ENDPOINT-5-R01 -> ENDPOINT-5-R02
```

必须检查：

- 所有 ENDPOINT round summary 存在。
- 所有 ENDPOINT stage summary 存在。
- final summary `.piko/summaries/worker_ENDPOINT-1-to-ENDPOINT-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- worker 状态应为 `ready_for_verify`。

必须检查 artifacts：

- Local approved endpoint contract artifact
- Local endpoint server/config artifact
- Explicit local opt-in artifact
- Live connector success verification artifact
- Normalized live signals artifact
- REAL funnel success handoff artifact
- Internal article handoff/readiness artifact
- Operator endpoint result artifact

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- ENDPOINT专项测试
- Local endpoint smoke
- Live connector success path probe
- REAL handoff success probe
- API/window probes if implemented
- Guardrail scan

核心验收点：

- local approved endpoint 返回 approved endpoint contract JSON。
- live connector success path 有 `real_collection_performed=true` evidence。
- 成功范围必须标明 local_approved_endpoint，不得声称 broad internet coverage。
- 不保存 raw response body、full posts、full comments、secrets。
- REAL handoff / article handoff 仍是 candidate/internal，publish_ready=false，publishing_performed=false。
- 其他 live connectors 未启用。

安全禁止项：

- 不得 crawler 或 scrape HTML。
- 不得发布、上传、部署、commit、push。
- 不得默认调用 LLM。
- 不得保存 raw/full source、secrets、credentials、token、cookie、API key、authorization。
- 不得绕过 verification 或放宽 Gate。

通过时：

- 生成 `.piko/summaries/verify_ENDPOINT-1-to-ENDPOINT-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=ENDPOINT-1-to-ENDPOINT-5`
  - `verification_summary_file=.piko/summaries/verify_ENDPOINT-1-to-ENDPOINT-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=ENDPOINT-1-to-ENDPOINT-5`

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- ENDPOINT-1 检查结果
- ENDPOINT-2 检查结果
- ENDPOINT-3 检查结果
- ENDPOINT-4 检查结果
- ENDPOINT-5 检查结果
- live success / scope 检查
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
