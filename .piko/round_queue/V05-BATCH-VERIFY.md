# Piko-verify Task Prompt: Verify V05-1 To V05-5 Real LangGraph Install Smoke

请一次性验证 V05-1 到 V05-5 连续批次。通过条件不是“必须安装成功”，而是 worker 是否按显式批准、受控安装/探测、版本记录、最小 smoke、Piko workflow smoke 和 guardrail 正确执行。失败或不可用必须诚实 blocked。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_V05-1-to-V05-5.md`

验证范围：

```text
V05-1-R01 -> V05-1-R02
V05-2-R01 -> V05-2-R02 -> V05-2-R03
V05-3-R01 -> V05-3-R02
V05-4-R01 -> V05-4-R02
V05-5-R01 -> V05-5-R02
```

必须检查：

- 所有 V05 round summary 存在。
- 所有 V05 stage summary 存在。
- final summary `.piko/summaries/worker_V05-1-to-V05-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- worker 状态应为：
  - `current_round=V05-1-to-V05-5`
  - `worker_status=ready_for_verify`
  - `verification_status=not_started`
  - `last_completed_round=V05-5-R02`
  - `worker_summary_file=.piko/summaries/worker_V05-1-to-V05-5.md`

必须检查 artifacts：

- V05 explicit install approval artifact
- Install command/result artifact
- Import/version probe artifact
- Minimal graph smoke artifact
- Piko workflow backend smoke artifact
- Final readiness / real data handoff artifact

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V05 artifact JSON parse probes
- LangGraph install/import/version tests or blocked status tests
- Minimal graph smoke tests
- Piko workflow backend smoke tests
- API/window probes if implemented
- Guardrail scan

核心验收点：

- Install/probe 需要 V05 explicit approval。
- 如果 LangGraph 成功，必须有 import、version、minimal smoke evidence。
- 如果失败，必须是 blocked_for_dependency/needs_fix，不能伪装成功。
- local_fixture fallback 必须仍可用。
- Piko workflow smoke 不得发布、部署、调用真实 LLM 或真实 source connectors。
- production_activation_allowed=false。

安全禁止项：

- 不得发布、部署、commit、push。
- 不得默认调用 LLM 或真实外部 source。
- 不得 vendor 外部源码。
- 不得保存 secrets、credentials、authorization。
- 不得绕过 verification 或放宽 Gate。
- 不得自动替换 active runtime。

通过时：

- 生成 `.piko/summaries/verify_V05-1-to-V05-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=V05-1-to-V05-5`
  - `verification_summary_file=.piko/summaries/verify_V05-1-to-V05-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=V05-1-to-V05-5`

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- V05-1 检查结果
- V05-2 检查结果
- V05-3 检查结果
- V05-4 检查结果
- V05-5 检查结果
- LangGraph success/blocked 状态
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
