# Round ID: REV-2-R03

Round Name: Live Smoke Summary Artifact

本轮目标:

Write a safe verification summary artifact for live endpoint verification.

本轮任务:
- 执行任务:
  - Write a summary artifact under `.piko/summaries/` or `artifacts/endpoint_verification/`.
  - Include status, mode, endpoint category, normalized counts, retained fields, skipped reason, and safety checks.
  - Do not include raw response bodies or secrets.
- 测试任务:
  - Test summary artifact redacts/skips prohibited fields.
  - Test skipped live smoke produces a clear skipped artifact.
  - Test successful mock-live smoke produces normalized counts and safety fields.
- 协作验收任务:
  - Worker summary must include summary artifact path.

允许修改:

- `packages/discovery/*`
- `artifacts/endpoint_verification/*`
- `tests/test_discovery_search.py`
- `.piko/summaries/worker_REV-2-R03.md`
- `.piko/summaries/worker_REV-2.md`
- `.piko/round_status.json`

禁止修改:

- Do not store endpoint raw body.
- Do not store secrets or authorization headers.
- Do not enter REV-3.

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`

完成定义:

- REV-2 live smoke, normalization/ranking probe, and summary artifact are complete.
- Stage summary `.piko/summaries/worker_REV-2.md` exists.
- Status is ready for Piko-verify with `next_round=REV-3-R01`.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
