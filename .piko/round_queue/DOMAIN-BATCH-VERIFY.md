# Piko-verify Task Prompt: Verify DOMAIN-1 To DOMAIN-5 General Plugin Boundary

请一次性验证 DOMAIN-1 到 DOMAIN-5 连续批次。重点是确认 Piko 的产品边界被明确锁定：Piko 是可插拔通用多 Agent 系统，gaming 只是一个 domain pack。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_DOMAIN-1-to-DOMAIN-5.md`

验证范围：

```text
DOMAIN-1-R01 -> DOMAIN-1-R02 -> DOMAIN-1-R03
DOMAIN-2-R01 -> DOMAIN-2-R02 -> DOMAIN-2-R03
DOMAIN-3-R01 -> DOMAIN-3-R02 -> DOMAIN-3-R03
DOMAIN-4-R01 -> DOMAIN-4-R02 -> DOMAIN-4-R03
DOMAIN-5-R01 -> DOMAIN-5-R02
```

必须检查：

- 所有 DOMAIN round summary 存在。
- 所有 DOMAIN stage summary 存在。
- final summary `.piko/summaries/worker_DOMAIN-1-to-DOMAIN-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- worker 状态应为 `ready_for_verify`。

必须检查 artifacts：

- Core/domain boundary artifact
- DomainPlugin v1 contract artifact
- Generic signal contract artifact
- Gaming domain pack artifact
- AI tools domain pack artifact
- Cross-domain routing artifact
- Domain-agnostic operator surface artifact
- Migration/readiness report

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- DOMAIN专项测试
- Domain artifact JSON parse probes
- Gaming and ai_tools domain fixture probes
- Cross-domain routing probes
- API/window probes if implemented
- Guardrail scan

核心验收点：

- Core contracts 不再把 Piko 绑定为 gaming-only。
- Gaming 被明确建模为 domain pack。
- AI tools 作为第二个非游戏 domain pack 可跑 fixture/probe。
- Cross-domain router 可以按 domain 选择 source schema、normalizer、scoring preset、content template。
- Operator surface 使用 domain-agnostic 文案，同时可以显示 domain-specific labels。
- 未删除或破坏现有 gaming tests。

安全禁止项：

- 不得发布、上传、部署、commit、push。
- 不得默认联网或默认调用 LLM。
- 不得保存 raw/full source、secrets、credentials、token、cookie、API key、authorization。
- 不得绕过 verification 或放宽 Gate。
- 不得把任何新 domain pack 自动生产启用。

通过时：

- 生成 `.piko/summaries/verify_DOMAIN-1-to-DOMAIN-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=DOMAIN-1-to-DOMAIN-5`
  - `verification_summary_file=.piko/summaries/verify_DOMAIN-1-to-DOMAIN-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=DOMAIN-1-to-DOMAIN-5`

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- DOMAIN-1 检查结果
- DOMAIN-2 检查结果
- DOMAIN-3 检查结果
- DOMAIN-4 检查结果
- DOMAIN-5 检查结果
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
