# Piko-worker Task Prompt: GROW-1 To GROW-5 Daily Growth Loop Batch

你现在执行 GROW-1 到 GROW-5，目标是建立 Piko v0.2 的每日成长闭环。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\GROW-INDEX.md`

然后按顺序执行：

```text
GROW-1-R01 -> GROW-1-R02
GROW-2-R01 -> GROW-2-R02 -> GROW-2-R03
GROW-3-R01 -> GROW-3-R02 -> GROW-3-R03
GROW-4-R01 -> GROW-4-R02
GROW-5-R01 -> GROW-5-R02
```

本批目标：

- 读取每日 piko-github 扫描结果。
- 标准化并去重候选 skill/agent/framework。
- 生成 CAP review report。
- 把候选分为 keep、augment、replace_candidate、deprecate_candidate、reject、story_only、watch。
- 生成 worker task draft。
- 生成 verify task draft。
- 打包 draft queue package。
- 提供只读 growth API/window。
- 明确 piko-skill 是对外内容线，不代表 Piko 吸收。
- 保持所有结果 proposal-only / draft-only。

重点输入：

- `C:\Users\pangv\.codex\automations\piko-github\memory.md`
- `artifacts/oss_research/*`
- `artifacts/capability_map/*`
- `artifacts/storytelling/*`

建议输出 artifacts：

- `artifacts/growth_loop/latest_scan_intake.json`
- `artifacts/growth_loop/latest_normalized_candidates.json`
- `artifacts/growth_loop/cap_review_policy.json`
- `artifacts/growth_loop/latest_cap_review_report.json`
- `artifacts/growth_loop/latest_capability_feedback.json`
- `artifacts/growth_loop/worker_task_draft_contract.json`
- `artifacts/growth_loop/verify_task_draft_contract.json`
- `artifacts/growth_loop/latest_draft_queue_package.json`
- `artifacts/growth_loop/latest_draft_queue_package.md`

执行规则：

- 每个 round 必须先读取对应 `GROW-*.md` 文件。
- 每完成一个 round，生成对应 `.piko/summaries/worker_<RoundID>.md`。
- 每完成一个 stage，生成 `.piko/summaries/worker_<StageID>.md`。
- 所有 stage 完成后，生成 `.piko/summaries/worker_GROW-1-to-GROW-5.md`。
- 完成 GROW-5-R02 后停止，等待 Piko-verify。

全局禁止项：

- 不要自动运行 generated worker tasks。
- 不要自动吸收 OSS candidates。
- 不要自动安装 plugins/connectors/dependencies/external repos。
- 不要发布、部署、commit、push。
- 不要默认联网。
- 不要默认调用 LLM。
- 不要绕过 Piko-verify 或放宽 Gate。
- 不要把 piko-skill 对外内容选题当成 Piko runtime adoption。

必须运行验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- Growth artifacts JSON parse probes
- CAP review decision probes
- Worker/verify draft safety probes
- API/window probes if implemented
- Guardrail scan

最终更新 `.piko/round_status.json`：

```text
current_round=GROW-1-to-GROW-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=GROW-5-R02
worker_summary_file=.piko/summaries/worker_GROW-1-to-GROW-5.md
next_round=null
```

最终输出格式：

- 修改了什么
- GROW-1 每个 round 状态
- GROW-2 每个 round 状态
- GROW-3 每个 round 状态
- GROW-4 每个 round 状态
- GROW-5 每个 round 状态
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
