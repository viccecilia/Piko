# Piko-verify Task Prompt: Verify V03-1 To V03-5 Practical Plugin Absorption Batch

请验证 V03-1 到 V03-5 连续批次。重点不是“是否研究了很多框架”，而是是否完成了一个尽快实战的、受控的成熟能力吸收试点。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_V03-1-to-V03-5.md`

验证范围：

```text
V03-1-R01 -> V03-1-R02
V03-2-R01 -> V03-2-R02 -> V03-2-R03
V03-3-R01 -> V03-3-R02
V03-4-R01 -> V03-4-R02
V03-5-R01 -> V03-5-R02
```

必须检查：

- 所有 V03 round summary 存在。
- 所有 V03 stage summary 存在。
- final summary `.piko/summaries/worker_V03-1-to-V03-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- worker 状态应为：
  - `current_round=V03-1-to-V03-5`
  - `worker_status=ready_for_verify`
  - `verification_status=not_started`
  - `last_completed_round=V03-5-R02`
  - `worker_summary_file=.piko/summaries/worker_V03-1-to-V03-5.md`

必须检查 artifacts：

- Practical candidate selection artifact
- LangGraph-style adapter contract artifact
- Local adapter fixture artifact
- Workflow trace artifact
- Approval packet artifact
- Operator trace/window artifact if implemented
- Practical readiness artifact

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V03 artifact JSON parse probes
- Adapter fixture tests
- Workflow trace tests
- API/window probes if implemented
- Guardrail scan

核心验收点：

- V03 选择了一个明确的 first practical candidate，而不是泛泛研究。
- 默认候选应能解释为什么最快服务 Piko 实战。
- Adapter pilot 即使不安装真实 LangGraph，也必须保留可替换的 contract 和 deterministic fixture。
- 真实 Piko workflow 场景必须跑通本地 fixture trace。
- Trace 必须显示 state、node/stage、Gate、retry/failure、verification handoff。
- 所有结果必须仍是 candidate/dry-run/internal。
- 不得自动安装、自动启用、自动替换 active runtime。

安全禁止项：

- 不得发布、部署、commit、push。
- 不得默认联网。
- 不得默认调用 LLM。
- 不得 vendor 外部源码。
- 不得保存 secrets、credentials、authorization。
- 不得绕过 verification 或放宽 Gate。
- 不得伪装真实 live success。

通过时：

- 生成 `.piko/summaries/verify_V03-1-to-V03-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=V03-1-to-V03-5`
  - `verification_summary_file=.piko/summaries/verify_V03-1-to-V03-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=V03-1-to-V03-5`
- 明确失败 artifact、失败 round、阻断原因和返工任务。

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- V03-1 检查结果
- V03-2 检查结果
- V03-3 检查结果
- V03-4 检查结果
- V03-5 检查结果
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
