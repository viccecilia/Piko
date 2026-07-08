# Round ID: CAP-0-R01

Round Name: Local Agent And Workflow Inventory

本轮目标:

扫描 Piko 本地已有 agents、workflow、gates、artifacts、API/window surface，建立第一版本地能力清单。

本轮任务:
- 执行任务:
  - 扫描并记录 Piko 当前本地能力：
    - SourceAgent
    - EvidenceAgent
    - RankingAgent
    - WriterAgent
    - EditorAgent
    - FactcheckAgent
    - VerificationGate
    - Discovery/Funnel/Watchlist
    - Endpoint verification
    - Publish readiness
    - Self-improvement/ledger guardrail
  - 输出 `artifacts/capability_map/local_capabilities.json`。
  - 每个 capability 至少包含：id、name、type、owner module、inputs、outputs、current status、tests、known limitations。
- 测试任务:
  - capability artifact JSON 可解析。
  - 至少覆盖 agents、workflow、API/window、verification 四类能力。
  - 不改变现有 runtime 行为。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-0-R01.md`。

允许修改:

- `packages/*`
- `apps/api/routes/*`
- `tests/*`
- `docs/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_CAP-0-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要删除或替换任何 agent。
- 不要默认联网。
- 不要安装插件。
- 不要发布、部署、commit、push。
- 不要绕过 verification。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- capability artifact JSON parse probe

完成定义:

- 本地能力清单存在且可解析。
- Piko 当前可用能力边界被记录。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
