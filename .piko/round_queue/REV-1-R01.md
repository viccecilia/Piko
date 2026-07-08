# Round ID: REV-1-R01

Round Name: Approved Endpoint Contract

本轮目标:

Define the approved JSON endpoint contract for live market verification.

本轮任务:
- 执行任务:
  - Document the required JSON shape for approved real endpoint payloads.
  - Define top-level fields for `games`, `questions`, `source`, `generated_at`, and optional `metadata`.
  - Define required hot game fields and player question fields.
  - Define prohibited fields and maximum snippet length.
  - Document that HTML pages and raw body endpoints are not approved.
- 测试任务:
  - Add tests validating an approved payload shape.
  - Add tests rejecting/disallowing payloads that include raw body fields or unsupported root structures.
- 协作验收任务:
  - Worker summary must include one valid endpoint JSON example and one rejected example.

允许修改:

- `docs/*`
- `packages/discovery/*`
- `tests/test_discovery_search.py`
- `.piko/summaries/worker_REV-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- Do not call live endpoints in this round.
- Do not add HTML scraping.
- Do not publish or deploy.

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`

完成定义:

- Approved JSON endpoint contract is documented and test-covered.
- Unsafe/raw payload shapes are rejected or clearly marked unsupported.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
