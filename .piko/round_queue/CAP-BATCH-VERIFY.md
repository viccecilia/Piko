# Piko-verify Task Prompt: Verify CAP-0 To CAP-4 Capability Map Batch

你现在验证 CAP-0 到 CAP-4 的能力图批次，不要只验单个 round。

验证范围：

```text
CAP-0-R01 -> CAP-0-R02 -> CAP-0-R03
CAP-1-R01 -> CAP-1-R02 -> CAP-1-R03
CAP-2-R01 -> CAP-2-R02 -> CAP-2-R03
CAP-3-R01 -> CAP-3-R02 -> CAP-3-R03
CAP-4-R01 -> CAP-4-R02
```

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_CAP-0-to-CAP-4.md`

必须检查：

- 每个 CAP round summary 存在：
  - `.piko/summaries/worker_CAP-0-R01.md` 到 `.piko/summaries/worker_CAP-4-R02.md`
- 每个 CAP stage summary 存在：
  - `.piko/summaries/worker_CAP-0.md` 到 `.piko/summaries/worker_CAP-4.md`
- final summary 存在：
  - `.piko/summaries/worker_CAP-0-to-CAP-4.md`
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- worker 状态应为：
  - `current_round=CAP-0-to-CAP-4`
  - `worker_status=ready_for_verify`
  - `verification_status=not_started`
  - `last_completed_round=CAP-4-R02`
  - `worker_summary_file=.piko/summaries/worker_CAP-0-to-CAP-4.md`

必须检查 artifacts：

- `artifacts/capability_map/current_inventory.json`
- `artifacts/capability_map/skill_connector_inventory.json`
- `artifacts/capability_map/latest_capability_map.json`
- `artifacts/capability_map/capability_scorecard.json`
- `artifacts/capability_map/replacement_policy.json`
- `artifacts/capability_map/capability_registry.json`
- `artifacts/capability_map/routing_policy.json`
- `artifacts/capability_map/autonomy_levels.json`
- `artifacts/capability_map/human_approval_contract.json`
- `artifacts/capability_map/continuous_update_loop.json`
- `artifacts/capability_map/latest_cap_review_report.json`

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- Capability artifact JSON parse probes
- Capability registry/routing probe if implemented
- API/window probes if implemented
- Guardrail scan

核心验收点：

CAP-0:

- Current local agent/workflow inventory 存在。
- Skill/connector inventory 存在。
- Latest capability map 存在。
- 能列出当前 Piko 的核心能力，例如 discovery、article pipeline、verification、storytelling、OSS learning、self-improvement proposal loop。

CAP-1:

- Evaluation metrics 存在。
- Replacement/deprecation policy 存在。
- Capability scorecard 存在。
- 替换建议只能是 candidate/proposal，不能自动执行。

CAP-2:

- Capability registry schema 存在。
- Routing policy 存在。
- 对 OSS candidates、STORY candidates、runtime candidates 有清晰分流。
- 如果新增 API/window preview，只能展示能力图，不得自动安装、替换或执行外部能力。

CAP-3:

- Autonomous workflow levels 存在。
- Human final approval contract 存在。
- Autonomous run report 存在。
- 必须明确 L5 full autonomous publish/deploy/credential/destructive replacement 禁用。

CAP-4:

- Continuous capability update loop 存在。
- latest CAP review report 存在。
- 能消费 OSS 队列输出的 candidate，但不能自动吸收。
- Final summary 存在。

安全禁止项：

- 不得自动安装 plugins/connectors。
- 不得自动替换、删除、禁用现有 agent/skill/tool。
- 不得自动应用 self-improvement patch。
- 不得发布、部署、commit、push。
- 不得默认联网。
- 不得默认调用 LLM。
- 不得绕过 verification 或放宽 Gate。
- 不得破坏 existing gaming discovery / article pipeline / STORY artifacts。
- 不得把 OSS 候选直接标记为已吸收。
- 人类最终确认必须保留在 publish、deploy、credential、paid service、license-risk、destructive replacement 之前。

通过时：

- 生成 `.piko/summaries/verify_CAP-0-to-CAP-4.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=CAP-0-to-CAP-4`
  - `verification_summary_file=.piko/summaries/verify_CAP-0-to-CAP-4.md`
  - `next_round=null`
  - UTF-8 no BOM

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=CAP-0-to-CAP-4`
- 明确失败 artifact、失败 round、阻断原因和返工任务。

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- CAP-0 检查结果
- CAP-1 检查结果
- CAP-2 检查结果
- CAP-3 检查结果
- CAP-4 检查结果
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
