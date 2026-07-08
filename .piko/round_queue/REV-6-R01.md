# Round ID: REV-6-R01

Round Name: Source-Backed Article Package Draft

本轮目标:

把 REV-5 选中的 safe candidate 接入 article/evidence workflow，生成一份 source-backed internal article package。若证据不足，必须生成 blocked/needs-evidence package，而不是硬写文章。

本轮任务:
- 执行任务:
  - 将 selected candidate 交给 SourceAgent -> EvidenceAgent -> RankingAgent -> WriterAgent -> EditorAgent -> FactcheckAgent -> VerificationGate 路径。
  - 生成或复用 article markdown/json artifact，保留 source_ids、evidence_card_ids、claim_trace、ranked_steps。
  - 文章必须包含 quick answer、what to try/check first、risk notes、sources、confidence。
  - 若 candidate 来自 mock-live/fixture，文章必须标明不是全网实时结论。
- 测试任务:
  - Article package 有 source trace 和 evidence trace。
  - Unsupported/high-risk/unanswered candidate 不会生成 normal publishable draft。
  - verification_report 存在且状态真实。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-6-R01.md`。

允许修改:

- `packages/workflows/*`
- `packages/discovery/*`
- `artifacts/article_drafts/*`
- `tests/test_discovery_search.py`
- `tests/test_content_benchmark.py`
- `docs/player_pain_discovery.md`
- `.piko/summaries/worker_REV-6-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要真实发布。
- 不要伪造 live success。
- 不要删除旧 artifacts 来逃避测试。
- 不要保存 raw/full source。
- 不要默认调用 LLM。
- 不要绕过 verification 或放宽 Gate。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m packages.workflows.article_pipeline`

完成定义:

- Internal article package 由多 Agent path 生成或安全阻断。
- source/evidence/claim trace 完整。
- publish_ready 仍按验证结果真实输出，默认不得自动发布。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
