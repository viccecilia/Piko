# Round ID: REV-1-R02

Round Name: Fixture Mirror Endpoint

本轮目标:

Create a local fixture/mirror endpoint payload that behaves like an approved real endpoint without touching the network.

本轮任务:
- 执行任务:
  - Add a local fixture JSON payload for real endpoint verification.
  - Include at least one hot game and multiple player questions.
  - Include at least one answered topic, one watchlist/unanswered topic, one conflict topic, and one high-risk blocked topic.
  - Include source categories matching at least Steam and one of Reddit/SERP/JP/KR.
- 测试任务:
  - Test fixture mirror loads and normalizes into `GameHeatSignal` and `PlayerQuestionSignal`.
  - Test fixture mirror can feed rankings without network.
  - Test retained fields exclude raw/full source content.
- 协作验收任务:
  - Worker summary must include fixture path, normalized game count, and normalized question count.

允许修改:

- `fixtures/*`
- `packages/discovery/*`
- `tests/test_discovery_search.py`
- `.piko/summaries/worker_REV-1-R02.md`
- `.piko/round_status.json`

禁止修改:

- Do not touch real endpoints.
- Do not save raw source bodies.
- Do not change publish behavior.

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`

完成定义:

- Local approved-endpoint mirror exists and can exercise the same normalization/ranking path as live endpoint data.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
