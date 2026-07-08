# Piko-verify Task Prompt: Verify V04-1 To V04-5 Real LangGraph Backend Approval Pilot

请一次性验证 V04-1 到 V04-5 连续批次。重点不是要求真实 backend 必然成功，而是验证 worker 是否正确执行了 approval、dependency、backend selector、workflow smoke 和 guardrail。如果缺批准或依赖失败，正确阻断也是通过路径之一。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_V04-1-to-V04-5.md`

验证范围：

```text
V04-1-R01 -> V04-1-R02
V04-2-R01 -> V04-2-R02 -> V04-2-R03
V04-3-R01 -> V04-3-R02
V04-4-R01 -> V04-4-R02
V04-5-R01 -> V04-5-R02
```

必须检查：

- 所有 V04 round summary 存在。
- 所有 V04 stage summary 存在。
- final summary `.piko/summaries/worker_V04-1-to-V04-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- worker 状态应为：
  - `current_round=V04-1-to-V04-5`
  - `worker_status=ready_for_verify`
  - `verification_status=not_started`
  - `last_completed_round=V04-5-R02`
  - `worker_summary_file=.piko/summaries/worker_V04-1-to-V04-5.md`

必须检查 artifacts：

- Dependency/license/safety review artifact
- Explicit approval artifact
- Install/probe result artifact
- Backend selector artifact
- LangGraph backend adapter artifact if implemented
- Workflow smoke trace artifact
- Activation readiness artifact

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V04 artifact JSON parse probes
- Backend selector tests
- LangGraph backend probe test or blocked status test
- Workflow smoke tests
- API/window probes if implemented
- Guardrail scan

核心验收点：

- 如果没有 approval，install/probe 必须 blocked_for_approval。
- 如果 approval 存在但依赖不可用，必须 blocked_for_dependency 或 needs_fix。
- 如果真实 backend 成功，必须有 import/version/smoke evidence，并且不替换 active runtime。
- 无论成功或阻断，local_fixture 必须仍可用。
- Workflow smoke 必须保持 Gate、verification、publish disabled 行为。
- activation_status 必须不是 production approved。

安全禁止项：

- 不得发布、部署、commit、push。
- 不得默认联网调用外部业务 API。
- 不得默认调用 LLM。
- 不得 vendor 外部源码。
- 不得保存 secrets、credentials、authorization。
- 不得绕过 verification 或放宽 Gate。
- 不得自动替换 active runtime。
- 不得伪装 real backend success。

通过时：

- 生成 `.piko/summaries/verify_V04-1-to-V04-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=V04-1-to-V04-5`
  - `verification_summary_file=.piko/summaries/verify_V04-1-to-V04-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=V04-1-to-V04-5`
- 明确失败 artifact、失败 round、阻断原因和返工任务。

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- V04-1 检查结果
- V04-2 检查结果
- V04-3 检查结果
- V04-4 检查结果
- V04-5 检查结果
- Backend success/blocked 状态
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
