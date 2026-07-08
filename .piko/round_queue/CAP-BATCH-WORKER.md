# Piko-worker Task Prompt: CAP-0 To CAP-4 Capability Map Batch

你现在执行 CAP-0 到 CAP-4。目标是建立 Piko 的“能力图”和“能力治理系统”：让 Piko 能持续记录自己有哪些 agent、skill、workflow、connector、OSS 候选、替换候选、风险边界和自动化等级。

本批次不是实现新外部能力，而是建立能力地图、评分体系、路由策略和持续优化闭环。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\CAP-INDEX.md`

然后按顺序执行：

```text
CAP-0-R01 -> CAP-0-R02 -> CAP-0-R03
CAP-1-R01 -> CAP-1-R02 -> CAP-1-R03
CAP-2-R01 -> CAP-2-R02 -> CAP-2-R03
CAP-3-R01 -> CAP-3-R02 -> CAP-3-R03
CAP-4-R01 -> CAP-4-R02
```

执行规则：

- 每个 round 必须先读取对应 `CAP-*.md` 文件。
- 每完成一个 round，生成对应 `.piko/summaries/worker_<RoundID>.md`。
- 每完成一个 stage，生成 `.piko/summaries/worker_<StageID>.md`。
- 所有 stage 完成后，生成 `.piko/summaries/worker_CAP-0-to-CAP-4.md`。
- 可以连续执行 CAP-0 到 CAP-4，但不能跳过任何 round。
- 如果某个 round 文件存在乱码，以本任务词和 `CAP-INDEX.md` 的 stage 目标为准，同时在 summary 中记录乱码风险。
- 最终停止，等待 Piko-verify。

本批目标：

- 建立当前 local agent/workflow inventory。
- 建立 available skills/connectors inventory。
- 建立 latest capability map。
- 建立 capability evaluation metrics。
- 建立 replacement/deprecation policy。
- 生成 capability scorecard。
- 建立 capability registry schema。
- 建立 capability routing policy。
- 提供可读的能力地图 API/window preview 或 artifact preview。
- 定义 autonomous workflow levels。
- 定义 human final approval contract。
- 定义 autonomous run report。
- 建立 continuous capability update loop。
- 能消费 OSS 队列输出的 candidates，但不能自动吸收。
- 能把候选能力分为 keep、augment、replace_candidate、deprecate_candidate、reject、story_only。

重点输入：

- `artifacts/oss_research/latest_upgrade_proposals.json`
- `artifacts/oss_research/capability_handoff_candidates.json`
- `artifacts/oss_research/latest_cap_queue_candidates.json`
- `artifacts/oss_research/latest_story_queue_candidates.json`
- 当前本地 skills：`C:\Users\pangv\.codex\skills`
- 当前 Piko packages / apps / tests / docs

建议输出 artifacts：

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

全局禁止项：

- 不要自动安装新 plugins/connectors。
- 不要自动替换、删除、禁用现有 agent/skill/tool。
- 不要自动应用 self-improvement patch。
- 不要发布、部署、commit、push。
- 不要默认联网。
- 不要默认调用 LLM。
- 不要绕过 verification 或放宽 Gate。
- 不要破坏现有 gaming discovery / article pipeline / STORY artifacts。
- 不要把 OSS 候选直接标记为已吸收。
- 人类最终确认仍然必须保留在 publish、deploy、credential、paid service、license-risk、destructive replacement 之前。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- Capability artifact JSON parse probes
- API/window probes if added
- Guardrail scan for auto-install, auto-replace, secrets, publish, deploy, commit, push, default network, default LLM, verification bypass

最终更新 `.piko/round_status.json`：

```text
current_round=CAP-0-to-CAP-4
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=CAP-4-R02
worker_summary_file=.piko/summaries/worker_CAP-0-to-CAP-4.md
next_round=null
```

最终输出格式：

- 修改了什么
- CAP-0 每个 round 状态
- CAP-1 每个 round 状态
- CAP-2 每个 round 状态
- CAP-3 每个 round 状态
- CAP-4 每个 round 状态
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
