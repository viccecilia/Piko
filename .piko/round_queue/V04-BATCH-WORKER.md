# Piko-worker Task Prompt: V04-1 To V04-5 Real LangGraph Backend Approval Pilot

请一次连续执行 V04-1 到 V04-5，然后停止等待 Piko-verify。目标是尽快进入真实 backend 试点，但必须保留硬门槛：没有批准就阻断，依赖失败就阻断，不能伪装成功。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\V04-INDEX.md`

执行顺序：

```text
V04-1-R01 -> V04-1-R02
V04-2-R01 -> V04-2-R02 -> V04-2-R03
V04-3-R01 -> V04-3-R02
V04-4-R01 -> V04-4-R02
V04-5-R01 -> V04-5-R02
```

本批次目标：

- 基于 V03 的 `langgraph_style_workflow_adapter`，做真实 LangGraph backend approval pilot。
- 建立 explicit approval artifact、dependency/license/safety review、受控安装/探测路径。
- 让同一条 workflow 可选择 `backend=local_fixture` 或 `backend=langgraph_backend`。
- 用 discovery -> evidence/ranking -> draft_handoff -> verification_gate 跑 smoke。
- 如果真实 backend 不可用，必须输出 blocked 状态，不要假装成功。
- 最终只输出 activation readiness，不要生产启用。

执行规则：

- 每个 round 执行前读取对应 `V04-*.md` 文件。
- 每完成一个 round，生成 `.piko/summaries/worker_<RoundID>.md`。
- 每完成一个 stage，生成 `.piko/summaries/worker_<StageID>.md`。
- 全部完成后生成 `.piko/summaries/worker_V04-1-to-V04-5.md`。
- 完成 V04-5-R02 后停止，等待 Piko-verify。

全局禁止项：

- 不替换 active runtime。
- 不发布、不部署、不 commit、不 push。
- 不使用 secrets、credentials、authorization。
- 不 vendor LangGraph 或其他外部仓库源码。
- 不默认调用 LLM。
- 不默认调用真实外部 connectors。
- 不绕过 verification，不放宽 Gate。
- 不伪装 real backend success。

允许的受控行为：

- 可以创建 approval artifact。
- 可以在 approval artifact 明确允许时进行 dependency availability/probe。
- 如果本地环境已有 LangGraph，可以进行受控 import/version/smoke。
- 如果需要安装依赖，必须由 approval artifact 明确允许，并记录 dependency、version、command、result、rollback note。
- 若安装不可行或失败，必须停止为 blocked 状态，并保留 local_fixture 可用。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V04 artifacts JSON parse probes
- LangGraph backend availability/probe test or blocked status test
- Backend selector tests
- Workflow smoke tests
- API/window probes if implemented
- Guardrail scan

最终更新 `.piko/round_status.json`：

```text
current_round=V04-1-to-V04-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=V04-5-R02
worker_summary_file=.piko/summaries/worker_V04-1-to-V04-5.md
next_round=null
```

最终输出格式：

- 修改了什么
- V04-1 每个 round 状态
- V04-2 每个 round 状态
- V04-3 每个 round 状态
- V04-4 每个 round 状态
- V04-5 每个 round 状态
- 真实 backend 状态：success / blocked_for_approval / blocked_for_dependency / needs_fix
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
