# Piko-verify Task Prompt: Verify CONNECTOR-1 To CONNECTOR-5

请一次性验证 CONNECTOR-1 到 CONNECTOR-5 连续批次。重点确认 Piko 是否建立了 domain-agnostic connector registry，并且没有默认真实采集、没有保存凭据、没有 crawler/scrape。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_CONNECTOR-1-to-CONNECTOR-5.md`

验证范围：

```text
CONNECTOR-1-R01 -> CONNECTOR-1-R02 -> CONNECTOR-1-R03
CONNECTOR-2-R01 -> CONNECTOR-2-R02
CONNECTOR-3-R01 -> CONNECTOR-3-R02 -> CONNECTOR-3-R03
CONNECTOR-4-R01 -> CONNECTOR-4-R02 -> CONNECTOR-4-R03
CONNECTOR-5-R01 -> CONNECTOR-5-R02
```

必须检查：

- 所有 CONNECTOR round summary 存在。
- 所有 CONNECTOR stage summary 存在。
- final summary `.piko/summaries/worker_CONNECTOR-1-to-CONNECTOR-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- worker 状态应为 `ready_for_verify`。

必须检查 artifacts：

- Connector registry contract artifact
- Connector manifest examples
- Source governance policy artifact
- Credential and permission boundary artifact
- Gaming connector pack artifact
- AI tools connector pack artifact
- Cross-domain connector routing artifact
- Collection dry-run plan/report artifact
- Operator connector surface artifact

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- CONNECTOR专项测试
- Connector artifact JSON parse probes
- Credential guardrail probes
- Domain connector routing probes
- Collection dry-run probes
- API/window probes if implemented
- Guardrail scan

核心验收点：

- Connector registry 是 domain-agnostic，不是 gaming-only。
- Gaming 和 ai_tools 都有 connector pack。
- Unknown domain/connector 安全失败。
- Credential policy 不保存 token/cookie/API key/authorization/secret。
- Collection plan 默认 dry-run，不真实采集。
- REAL 缺 endpoint 被表达为 blocked_for_endpoint，不伪装成功。
- 没有 crawler、HTML scrape、raw/full source 保存。

安全禁止项：

- 不得发布、上传、部署、commit、push。
- 不得默认联网或默认调用 LLM。
- 不得保存 raw/full source、secrets、credentials、token、cookie、API key、authorization。
- 不得绕过 verification 或放宽 Gate。
- 不得自动启用 connector。

通过时：

- 生成 `.piko/summaries/verify_CONNECTOR-1-to-CONNECTOR-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=CONNECTOR-1-to-CONNECTOR-5`
  - `verification_summary_file=.piko/summaries/verify_CONNECTOR-1-to-CONNECTOR-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=CONNECTOR-1-to-CONNECTOR-5`

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- CONNECTOR-1 检查结果
- CONNECTOR-2 检查结果
- CONNECTOR-3 检查结果
- CONNECTOR-4 检查结果
- CONNECTOR-5 检查结果
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
