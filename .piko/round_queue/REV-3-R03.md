# Round ID: REV-3-R03

Round Name: Endpoint Trace Artifact And Window Surface

本轮目标:

把真实/模拟真实 endpoint 的采集轨迹展示到本地窗口和 artifact 摘要中，让操作员能看到搜了哪些平台、返回多少、丢弃多少、哪些进入漏斗。

本轮任务:
- 执行任务:
  - 扩展 endpoint verification artifact，加入 source-level stats：requested source、normalized count、discarded count、skip reason、mode、real_collection_performed。
  - 扩展 `/discovery/funnel-trace` 或新增 endpoint trace API，显示 source scan -> normalized signals -> funnel handoff。
  - 扩展 `/discovery/funnel-window`，显示中文 source trace：平台、模式、返回数量、丢弃数量、是否真实采集。
  - 页面必须明确显示默认离线、真实采集需要 opt-in。
- 测试任务:
  - API probe 能看到 source-level trace fields。
  - HTML probe 能看到“真实采集”“默认离线”“丢弃记录”“进入漏斗”等中文文案。
  - Artifact 不包含 raw body / full posts / secrets。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-3-R03.md`。
  - 生成 stage summary `.piko/summaries/worker_REV-3.md`。

允许修改:

- `apps/api/routes/discovery.py`
- `packages/discovery/*`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`
- `.piko/summaries/worker_REV-3-R03.md`
- `.piko/summaries/worker_REV-3.md`
- `.piko/round_status.json`

禁止修改:

- 不要默认触网。
- 不要保存 raw/full source。
- 不要发布、部署、commit、push。
- 不要绕过 verification 或放宽 Gate。
- 不要进入不相关队列。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m packages.discovery.real_endpoint_verify --fixture --write-artifact`

完成定义:

- REV-3 三个 round summary 和 stage summary 都存在。
- Source trace 可在 API/window/artifact 中看到。
- 默认离线、安全 skip、无 raw source 保留。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
