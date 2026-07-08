# Piko-worker Task Prompt: V05-1 To V05-5 Real LangGraph Install Smoke

请一次连续执行 V05-1 到 V05-5，然后停止等待 Piko-verify。目标是显式批准并尝试真实安装/探测 LangGraph，记录版本、import、最小 graph smoke，再用同一条 Piko workflow 跑 backend smoke。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\V05-INDEX.md`

执行顺序：

```text
V05-1-R01 -> V05-1-R02
V05-2-R01 -> V05-2-R02 -> V05-2-R03
V05-3-R01 -> V05-3-R02
V05-4-R01 -> V05-4-R02
V05-5-R01 -> V05-5-R02
```

本批次目标：

- 基于 V04 的 `blocked_for_dependency`，生成 V05 显式安装批准 artifact。
- 受控执行 LangGraph dependency install/probe，记录 command、version、import evidence、result、rollback note。
- 跑最小 graph smoke。
- 让 Piko workflow 使用 `backend=langgraph_backend` 跑 smoke。
- 如果任何步骤失败，必须正确 blocked/needs_fix，不伪装成功。
- 生产启用仍保持 not_approved_for_production。

全局禁止项：

- 不替换 active runtime。
- 不发布、不部署、不 commit、不 push。
- 不使用 secrets、credentials、authorization。
- 不 vendor LangGraph 源码。
- 不默认调用真实 LLM。
- 不默认调用真实 source connectors。
- 不绕过 verification，不放宽 Gate。
- 不伪装 LangGraph backend success。

允许的受控行为：

- 可以按 V05 approval artifact 执行最小依赖安装或本地 dependency probe。
- 可以记录 pip/install command 和退出状态。
- 可以 import LangGraph 并读取版本。
- 可以运行本地纯 fixture graph smoke。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- V05 artifacts JSON parse probes
- LangGraph install/import/version tests or blocked status tests
- Minimal graph smoke tests
- Piko workflow backend smoke tests
- Guardrail scan

最终更新 `.piko/round_status.json`：

```text
current_round=V05-1-to-V05-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=V05-5-R02
worker_summary_file=.piko/summaries/worker_V05-1-to-V05-5.md
next_round=null
```

最终输出格式：

- 修改了什么
- V05-1 每个 round 状态
- V05-2 每个 round 状态
- V05-3 每个 round 状态
- V05-4 每个 round 状态
- V05-5 每个 round 状态
- LangGraph 状态：success / blocked_for_dependency / needs_fix
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议：真实数据 batch
