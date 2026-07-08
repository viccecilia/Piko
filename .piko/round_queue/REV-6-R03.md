# Round ID: REV-6-R03

Round Name: Operator Result Surface And Final Batch Summary

本轮目标:

把 REV-3 到 REV-6 的结果汇总到本地 operator/client surface 中，让操作员能一眼看到：当前热游、棘手问题、解决方案线索、文章包状态、配图计划、发布准备状态。

本轮任务:
- 执行任务:
  - 扩展本地窗口或新增 API，展示 latest real market funnel report 和 article package readiness。
  - 页面必须包含中文栏目：
    - 当前最热游戏
    - 棘手玩家问题
    - 已搜索到的解决方案线索
    - 已生成文章包
    - 配图/媒体计划
    - 发布准备状态
  - 明确显示 `publishing_performed=false`，以及“需要后续显式发布 Stage 才能真正发布”。
  - 写最终 batch summary `.piko/summaries/worker_REV-3-to-REV-6.md`。
  - 更新 `.piko/round_status.json`：`current_round=REV-3-to-REV-6`、`worker_status=ready_for_verify`、`verification_status=not_started`、`last_completed_round=REV-6-R03`、`last_verified_round=REV-2`、`worker_summary_file=.piko/summaries/worker_REV-3-to-REV-6.md`、`next_round=null`。
- 测试任务:
  - API/window probe 确认六个中文栏目可见。
  - Full pytest 通过。
  - Article pipeline 通过或安全阻断且报告原因。
  - Live smoke 默认 skip；如 env 配置则显式 opt-in 运行并记录真实结果。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-6-R03.md`。
  - 生成 `.piko/summaries/worker_REV-6.md`。
  - 生成 `.piko/summaries/worker_REV-3-to-REV-6.md`。

允许修改:

- `apps/api/routes/discovery.py`
- `apps/api/routes/pages.py`
- `apps/web/pages/*`
- `packages/discovery/*`
- `packages/workflows/*`
- `artifacts/discovery_reports/*`
- `artifacts/article_drafts/*`
- `artifacts/publish_readiness/*`
- `tests/test_discovery_search.py`
- `tests/test_content_benchmark.py`
- `docs/player_pain_discovery.md`
- `docs/current_state.md`
- `.piko/summaries/worker_REV-6-R03.md`
- `.piko/summaries/worker_REV-6.md`
- `.piko/summaries/worker_REV-3-to-REV-6.md`
- `.piko/round_status.json`

禁止修改:

- 不要真实发布、部署、commit、push。
- 不要新增一键公开发布副作用。
- 不要默认触网。
- 不要 crawler、scrape HTML 或保存 raw/full source。
- 不要下载外部图片。
- 不要默认调用 LLM、translation API 或 image generation。
- 不要绕过 verification 或放宽 Gate。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --fixture`
- `python -m packages.discovery.real_endpoint_verify --fixture --write-artifact`
- `python -m packages.discovery.real_endpoint_verify --live`
- `python -m packages.workflows.article_pipeline`
- API/window probes for the final result surface

完成定义:

- REV-3 到 REV-6 所有 round summary、stage summary、final batch summary 都存在。
- 最终结果 surface 能回答用户四个问题。
- 系统如实区分 fixture/mock-live/real-source。
- 没有发布、部署、raw source、crawler、默认 LLM 或图片下载副作用。
- `round_status.json` 进入 ready_for_verify，等待 Piko-verify 做整体验收。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
