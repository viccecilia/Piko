# Round ID: LIVE-1-R03

Round Name: Live Result Artifact And Operator Surface

本轮目标:

把 LIVE-1 的真实或 skipped 结果写入安全 artifact，并展示到 operator surface，让用户能明确看到：是否真实联网、拿到多少游戏/问题、哪些进入排行、哪些被丢弃、为什么没有发布。

本轮任务:
- 执行任务:
  - 写入或更新 `artifacts/endpoint_verification/latest_endpoint_verification.json`。
  - 如有 live success，artifact 必须包含：
    - `mode=real-source`
    - `real_collection_performed=true`
    - normalized game/question counts
    - discarded/unsupported counts
    - source-level stats
    - retained fields
    - safety flags
  - 如 live skipped，artifact 必须包含 skipped reason 和 missing configuration。
  - 扩展 `/discovery/operator-result` 或相关窗口，显示 LIVE-1 状态：
    - 真实联网状态
    - Endpoint 配置状态
    - 热门游戏预览
    - 玩家问题预览
    - 安全护栏结果
    - 发布状态：未发布
  - 写 stage summary `.piko/summaries/worker_LIVE-1.md`。
  - 更新 `.piko/round_status.json`：
    - `current_round=LIVE-1`
    - `worker_status=ready_for_verify`
    - `verification_status=not_started`
    - `last_completed_round=LIVE-1-R03`
    - `last_verified_round=REV-3-to-REV-6`
    - `worker_summary_file=.piko/summaries/worker_LIVE-1.md`
    - `next_round=null`
    - UTF-8 no BOM
- 测试任务:
  - Artifact JSON parse 通过。
  - Artifact 不含 raw body/full source/secrets。
  - API/window probe 显示 LIVE-1 状态。
  - Full pytest 通过。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-1-R03.md`。
  - 生成 `.piko/summaries/worker_LIVE-1.md`。

允许修改:

- `apps/api/routes/discovery.py`
- `packages/discovery/*`
- `artifacts/endpoint_verification/*`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`
- `docs/current_state.md`
- `.piko/summaries/worker_LIVE-1-R03.md`
- `.piko/summaries/worker_LIVE-1.md`
- `.piko/round_status.json`

禁止修改:

- 不要发布、部署、commit、push。
- 不要 crawler、scrape HTML 或保存 raw/full source。
- 不要下载/生成图片。
- 不要默认调用 LLM 或 translation API。
- 不要绕过 verification 或放宽 Gate。
- 不要把 skipped live 标成 real-source success。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --fixture`
- `python -m packages.discovery.real_endpoint_verify --fixture --write-artifact`
- `python -m packages.discovery.real_endpoint_verify --live`
- API/window probes for LIVE-1 result surface

完成定义:

- LIVE-1 所有 round summary 和 stage summary 都存在。
- Endpoint verification artifact 能真实说明 live passed/skipped/failed。
- Operator surface 能展示 LIVE-1 结果。
- 没有发布、部署、raw source、crawler、默认 LLM、translation API 或图片副作用。
- `round_status.json` 进入 ready_for_verify。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
