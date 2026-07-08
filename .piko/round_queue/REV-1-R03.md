# Round ID: REV-1-R03

Round Name: Endpoint Verification CLI

本轮目标:

Add an operator CLI that verifies approved endpoint payloads in fixture mode and live mode.

本轮任务:
- 执行任务:
  - Add a CLI/module for endpoint verification, for example `python -m packages.discovery.real_endpoint_verify`.
  - Support fixture/mirror mode by default.
  - Support live URL only with explicit opt-in env vars.
  - Output status, mode, source count, normalized game/question counts, retained fields, skipped reason, and safety flags.
- 测试任务:
  - Test CLI fixture mode passes without network.
  - Test live mode skips without opt-in.
  - Test live mode skips or fails clearly without endpoint URL.
- 协作验收任务:
  - Worker summary must include CLI commands and sample outputs.

允许修改:

- `packages/discovery/*`
- `tests/test_discovery_search.py`
- `.piko/summaries/worker_REV-1-R03.md`
- `.piko/summaries/worker_REV-1.md`
- `.piko/round_status.json`

禁止修改:

- Do not make live mode default.
- Do not store full endpoint response bodies.
- Do not enter REV-2.

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --fixture`

完成定义:

- REV-1 contract, fixture mirror, and verification CLI are complete.
- Stage summary `.piko/summaries/worker_REV-1.md` exists.
- Status is ready for Piko-verify with `next_round=REV-2-R01`.

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
