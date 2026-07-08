# Piko-worker Task Prompt: DOMAIN-1 To DOMAIN-5 General Plugin Boundary

请一次连续执行 DOMAIN-1 到 DOMAIN-5，然后停止等待 Piko-verify。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\DOMAIN-INDEX.md`

执行顺序：

```text
DOMAIN-1-R01 -> DOMAIN-1-R02 -> DOMAIN-1-R03
DOMAIN-2-R01 -> DOMAIN-2-R02 -> DOMAIN-2-R03
DOMAIN-3-R01 -> DOMAIN-3-R02 -> DOMAIN-3-R03
DOMAIN-4-R01 -> DOMAIN-4-R02 -> DOMAIN-4-R03
DOMAIN-5-R01 -> DOMAIN-5-R02
```

本批次目标：

- 明确 Piko 的产品边界：Piko 是通用可插拔多 Agent 系统，不是单做游戏。
- 把 gaming 从 core 概念里抽为第一个 domain pack。
- 新增 ai_tools domain pack，证明 Piko 可套用非游戏领域。
- 建立 domain-agnostic workflow routing、signal contract、content package 和 operator surface。
- 保持所有真实外部数据和发布动作关闭。

核心边界：

- Core 不写死 game、player、guide、Steam、Reddit 等游戏专属概念。
- Core 只认 domain、source_signal、need_cluster、evidence、workflow_trace、content_package、distribution_package、verify_gate。
- 游戏相关词汇只能出现在 gaming domain pack、fixture、docs 或 domain-specific adapter 中。
- AI 工具相关词汇只能出现在 ai_tools domain pack、fixture、docs 或 domain-specific adapter 中。

全局禁止项：

- 不删除现有 gaming 能力。
- 不默认联网。
- 不默认调用 LLM。
- 不发布、不上传、不部署、不 commit、不 push。
- 不保存 raw/full source。
- 不保存 secrets、credentials、token、cookie、API key、authorization。
- 不绕过 verification，不放宽 Gate。
- 不把 ai_tools 或 gaming 自动标记为 production active，除非已有验证批准。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- DOMAIN 专项测试
- Domain artifact JSON parse probes
- Gaming / ai_tools fixture probes
- Cross-domain routing probes
- API/window probes if implemented
- Guardrail scan

最终更新 `.piko/round_status.json`：

```text
current_round=DOMAIN-1-to-DOMAIN-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=DOMAIN-5-R02
worker_summary_file=.piko/summaries/worker_DOMAIN-1-to-DOMAIN-5.md
next_round=null
```

最终输出格式：

- 修改了什么
- DOMAIN-1 每个 round 状态
- DOMAIN-2 每个 round 状态
- DOMAIN-3 每个 round 状态
- DOMAIN-4 每个 round 状态
- DOMAIN-5 每个 round 状态
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
