# Round ID: REV-5-R01

Round Name: Safe Topic Candidate Selection

本轮目标:

从 endpoint-fed 漏斗结果中选择一个最适合写作的安全 topic，并证明 watchlist/high-risk/conflict topic 不会被误送入普通文章生成。

本轮任务:
- 执行任务:
  - 选择最高分 safe `publish_candidate` 作为 internal article candidate。
  - 如果没有 safe publish candidate，则选择一个清楚的 blocked/watchlist 示例，并说明为什么不能写。
  - Candidate 必须保留 game_id、game_name、need_key、decision、answer_status、risk_level、source hints、source trace、mode。
  - Candidate 输出必须 `publish_ready=false`、`requires_evidence_pipeline=true`、`candidate_only=true`。
- 测试任务:
  - publish_candidate 可被选择。
  - watchlist/high-risk 不进入 normal draft。
  - conflict topic 只能进入 synthesis/conflict path，不能伪装成确定解法。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-5-R01.md`。

允许修改:

- `packages/discovery/*`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`
- `.piko/summaries/worker_REV-5-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要发布。
- 不要绕过 evidence pipeline。
- 不要把 skipped/mock-live 当真实采集。
- 不要默认调用 LLM。
- 不要放宽 Gate。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`

完成定义:

- Endpoint-fed topic selection 安全、可追溯、candidate-only。
- 不安全 topic 被正确阻断或转入监控/冲突解释。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
