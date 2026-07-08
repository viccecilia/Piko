# Round ID: OSS-4-R02

Round Name: Domain-Aware API And CLI Probe

本轮目标:

为未来可插拔 domain 提供最小 API/CLI 探针，但不触发真实采集或发布。

本轮任务:
- 执行任务:
  - 增加或更新 domain-aware CLI/API probe。
  - 支持 default/gaming/demo/unknown domain 的安全响应。
  - 输出响应中必须包含 candidate_only、publish_ready=false、real_collection_performed=false。
- 测试任务:
  - CLI/API probe 覆盖 default domain、gaming、demo domain、unknown domain。
  - unknown domain 不能 fallback 到危险行为。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-4-R02.md`。

允许修改:

- `packages/*`
- `apps/api/routes/*`
- `tests/*`
- `docs/*`
- `.piko/summaries/worker_OSS-4-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要新增真实采集默认行为。
- 不要触发 article generation。
- 不要发布或部署。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- Domain CLI/API probes。

完成定义:

- 可插拔 domain 有最小可观察入口，但仍安全离线。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
