# Piko-verify Task Prompt: Verify GROW-1 To GROW-5 Daily Growth Loop Batch

你现在验证 GROW-1 到 GROW-5 的每日成长闭环批次，不要只验单个 round。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_GROW-1-to-GROW-5.md`

验证范围：

```text
GROW-1-R01 -> GROW-1-R02
GROW-2-R01 -> GROW-2-R02 -> GROW-2-R03
GROW-3-R01 -> GROW-3-R02 -> GROW-3-R03
GROW-4-R01 -> GROW-4-R02
GROW-5-R01 -> GROW-5-R02
```

必须检查：

- 所有 GROW round summary 存在。
- 所有 GROW stage summary 存在。
- final summary `.piko/summaries/worker_GROW-1-to-GROW-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- worker 状态应为：
  - `current_round=GROW-1-to-GROW-5`
  - `worker_status=ready_for_verify`
  - `verification_status=not_started`
  - `last_completed_round=GROW-5-R02`
  - `worker_summary_file=.piko/summaries/worker_GROW-1-to-GROW-5.md`

必须检查 artifacts：

- `artifacts/growth_loop/latest_scan_intake.json`
- `artifacts/growth_loop/latest_normalized_candidates.json`
- `artifacts/growth_loop/cap_review_policy.json`
- `artifacts/growth_loop/latest_cap_review_report.json`
- `artifacts/growth_loop/latest_capability_feedback.json`
- `artifacts/growth_loop/worker_task_draft_contract.json`
- `artifacts/growth_loop/verify_task_draft_contract.json`
- `artifacts/growth_loop/latest_draft_queue_package.json`
- `artifacts/growth_loop/latest_draft_queue_package.md`

必须运行验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- Growth artifacts JSON parse probes
- CAP review decision probes
- Worker/verify task draft safety probes
- API/window probes if implemented
- Guardrail scan

核心验收点：

GROW-1:

- 能读取 piko-github memory 或 OSS artifacts。
- 能区分当天结果和最近一次 fallback。
- 候选被标准化和去重。

GROW-2:

- CAP review policy 存在。
- CAP review report 有 decision、reason、tests、risk、next_action。
- 不把候选自动变成 active capability。

GROW-3:

- Worker task draft contract 存在。
- Verify task draft contract 存在。
- Draft queue package 存在。
- 所有任务均为 `draft_only`，不得自动写入正式 `.piko/round_queue`。

GROW-4:

- 如实现 API/window，必须只读。
- `/growth/status` 和 `/growth/window` 不得触发扫描、安装、执行、发布。
- HTML 不得引用外部 CDN。

GROW-5:

- 文档说明 piko-github、CAP Review、draft-only、human approval、piko-skill separation。
- Final summary 存在。

安全禁止项：

- 不得自动运行 generated worker tasks。
- 不得自动吸收 OSS candidates。
- 不得自动安装 plugins/connectors/dependencies/external repos。
- 不得发布、部署、commit、push。
- 不得默认联网。
- 不得默认调用 LLM。
- 不得绕过 verification 或放宽 Gate。
- 不得把 piko-skill 对外内容选题当成 Piko runtime adoption。

通过时：

- 生成 `.piko/summaries/verify_GROW-1-to-GROW-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=GROW-1-to-GROW-5`
  - `verification_summary_file=.piko/summaries/verify_GROW-1-to-GROW-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=GROW-1-to-GROW-5`
- 明确失败 artifact、失败 round、阻断原因和返工任务。

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- GROW-1 检查结果
- GROW-2 检查结果
- GROW-3 检查结果
- GROW-4 检查结果
- GROW-5 检查结果
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
