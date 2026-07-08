# Piko-verify Task Prompt: Verify V02-1 To V02-5 Runtime Growth Batch

你现在验证 V02-1 到 V02-5 的 runtime growth 批次，不要只验单个 round。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_V02-1-to-V02-5.md`

验证范围：

```text
V02-1-R01 -> V02-1-R02
V02-2-R01 -> V02-2-R02 -> V02-2-R03
V02-3-R01 -> V02-3-R02 -> V02-3-R03
V02-4-R01 -> V02-4-R02 -> V02-4-R03
V02-5-R01 -> V02-5-R02
```

必须检查：

- 所有 V02 round summary 存在。
- 所有 V02 stage summary 存在。
- final summary `.piko/summaries/worker_V02-1-to-V02-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- worker 状态应为：
  - `current_round=V02-1-to-V02-5`
  - `worker_status=ready_for_verify`
  - `verification_status=not_started`
  - `last_completed_round=V02-5-R02`
  - `worker_summary_file=.piko/summaries/worker_V02-1-to-V02-5.md`

必须检查 artifacts：

- `artifacts/v02_runtime/approval_packet_contract.json`
- `artifacts/v02_runtime/latest_materialization_preview.json`
- DomainPlugin runtime artifacts if generated
- AI tools demo domain fixture artifacts if generated
- `artifacts/v02_runtime/framework_candidate_comparison.json`
- `artifacts/v02_runtime/eval_pack_contract.json`
- `artifacts/v02_runtime/latest_run_trace.json`
- `artifacts/v02_runtime/real_pilot_readiness.json`

必须运行验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V02 artifacts JSON parse probes
- Plugin runtime fixture tests
- Adapter contract tests
- Eval/trace artifact tests
- API/window probes if implemented
- Guardrail scan

核心验收点：

- V02-1: 无 approval 时不得 materialize executable queue。
- V02-2: DomainPlugin runtime 不破坏 gaming，ai_tools demo 不触网不发布。
- V02-3: Adapter contract 不安装外部框架，不默认 LLM/API，不替换 runtime。
- V02-4: Eval/trace 只用本地 artifact，不保存 secrets/raw source，不接外部 SaaS。
- V02-5: Real pilot readiness 无 endpoint 时必须 blocked/skipped，不得伪装 live success。

安全禁止项：

- 不得执行 draft tasks。
- 不得自动吸收 OSS candidates。
- 不得自动安装 dependencies/plugins/connectors/repos/frameworks。
- 不得发布、部署、commit、push。
- 不得默认联网。
- 不得默认调用 LLM。
- 不得替换 active capabilities。
- 不得绕过 verification 或放宽 Gate。
- 不得保存 secrets/raw source body。

通过时：

- 生成 `.piko/summaries/verify_V02-1-to-V02-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=V02-1-to-V02-5`
  - `verification_summary_file=.piko/summaries/verify_V02-1-to-V02-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=V02-1-to-V02-5`
- 明确失败 artifact、失败 round、阻断原因和返工任务。

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- V02-1 检查结果
- V02-2 检查结果
- V02-3 检查结果
- V02-4 检查结果
- V02-5 检查结果
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
