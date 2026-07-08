# Round ID: OSS-3-R01

Round Name: Mature Agent Framework Adapter Proposal

本轮目标:

围绕“不要训练模型、不要完全自研 agent runtime、用成熟 agent 框架”的方向，设计成熟框架适配提案。

本轮任务:
- 执行任务:
  - 根据 OSS proposals，识别可评估的成熟 agent/workflow 框架候选，例如 LangGraph、OpenAI Agents SDK、CrewAI、LlamaIndex。
  - 定义 `AgentRuntimeAdapter` 或同等接口草案：run_task、tool_policy、state_contract、evidence_contract、verification_contract。
  - 明确 Piko 业务规则、证据链、Gate、验证体系仍由 Piko 控制。
  - 保存 `artifacts/oss_research/agent_framework_adapter_proposal.json`。
- 测试任务:
  - 验证 proposal JSON 可解析。
  - 验证接口草案不绑定单一供应商。
  - 验证没有默认调用外部 LLM/API。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-3-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/oss_research/*`
- `.piko/summaries/worker_OSS-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要安装或启用真实 agent 框架。
- 不要默认调用 LLM。
- 不要绕过 Piko verification。

必须运行的验证:

- Adapter proposal JSON parse probe。
- Default LLM/API guardrail scan。

完成定义:

- 成熟 agent 框架接入方向明确，但仍是 proposal，不改变运行时。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
