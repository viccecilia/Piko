# Piko-worker Task Prompt: V03-1 To V03-5 Practical Plugin Absorption Batch

你现在执行 V03-1 到 V03-5。目标是尽快让 Piko 具备可实战的第一条成熟能力吸收路径，不要做大而全研究。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\V03-INDEX.md`

执行顺序：

```text
V03-1-R01 -> V03-1-R02
V03-2-R01 -> V03-2-R02 -> V03-2-R03
V03-3-R01 -> V03-3-R02
V03-4-R01 -> V03-4-R02
V03-5-R01 -> V03-5-R02
```

本批次目标：

- 选择一个最适合尽快实战的成熟能力候选。
- 默认首选 LangGraph-style workflow adapter，因为它直接解决 workflow、state、Gate、retry、trace 和 multi-agent handoff。
- 基于 V02 的 AgentRuntimeAdapter / DomainPlugin 基础，做一个受控 adapter pilot。
- 用一个真实 Piko 工作流场景跑通本地 fixture：discovery candidate -> evidence/ranking -> article package handoff -> verification trace。
- 输出 operator 能看懂的 trace 和 approval packet。
- 全部保持 candidate/dry-run/internal，不自动启用，不发布。

执行规则：

- 每个 round 执行前读取对应 `V03-*.md` 文件。
- 每完成一个 round，生成 `.piko/summaries/worker_<RoundID>.md`。
- 每完成一个 stage，生成 `.piko/summaries/worker_<StageID>.md`。
- 全部完成后生成 `.piko/summaries/worker_V03-1-to-V03-5.md`。
- 完成 V03-5-R02 后停止，等待 Piko-verify。

全局禁止项：

- 不自动安装 LangGraph、CrewAI、OpenAI Agents SDK 或任何外部依赖。
- 不 vendor 外部仓库源码。
- 不替换 active runtime / active capability。
- 不默认联网。
- 不默认调用 LLM。
- 不发布、不部署、不 commit、不 push。
- 不使用 secrets、credentials、authorization。
- 不绕过 verification，不放宽 Gate。
- 不伪装 real/live success。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V03 artifacts JSON parse probes
- Adapter fixture tests
- Workflow trace tests
- API/window probes if implemented
- Guardrail scan

最终更新 `.piko/round_status.json`：

```text
current_round=V03-1-to-V03-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=V03-5-R02
worker_summary_file=.piko/summaries/worker_V03-1-to-V03-5.md
next_round=null
```

最终输出格式：

- 修改了什么
- V03-1 每个 round 状态
- V03-2 每个 round 状态
- V03-3 每个 round 状态
- V03-4 每个 round 状态
- V03-5 每个 round 状态
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
