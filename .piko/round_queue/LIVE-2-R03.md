# Round ID: LIVE-2-R03

Round Name: Real Live Result Surface And Handoff

本轮目标:

把 LIVE-2 真实 live smoke 结果展示到 operator/API surface，并生成下一步候选 handoff：真实热游、真实问题、候选 topic、不能发布原因。

本轮任务:
- 执行任务:
  - 扩展 `/discovery/operator-result` 或相关 API/window，使其显示 LIVE-2:
    - live_endpoint_status
    - mode
    - real_collection_performed
    - normalized_game_count
    - normalized_question_count
    - top hot games preview
    - hot question buckets preview
    - artifact path
    - publishing_performed=false
  - 若 R02 成功，生成 live handoff summary，说明哪些真实 topic 可以进入下一阶段 source/evidence pipeline。
  - 若 R02 blocked/failed，页面必须显示失败/阻塞原因，而不是旧 mock-live 结果。
  - 写 stage summary `.piko/summaries/worker_LIVE-2.md`。
  - 更新 `.piko/round_status.json`：
    - 成功 ready for verify:
      - `current_round=LIVE-2`
      - `worker_status=ready_for_verify`
      - `verification_status=not_started`
      - `last_completed_round=LIVE-2-R03`
      - `last_verified_round=LIVE-1`
      - `worker_summary_file=.piko/summaries/worker_LIVE-2.md`
      - `next_round=null`
    - 如果 endpoint 缺失:
      - `worker_status=blocked_for_endpoint`
      - `verification_status=not_started`
      - `next_round=LIVE-2-R01`
      - 清楚写明需要 `PIKO_APPROVED_ENDPOINT_URL`
- 测试任务:
  - API/window probe 显示 LIVE-2 live fields。
  - Artifact JSON parse 通过。
  - Full pytest 通过。
  - Safety scan 无 raw/full source/secrets。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-2-R03.md`。
  - 生成 `.piko/summaries/worker_LIVE-2.md`。

允许修改:

- `apps/api/routes/discovery.py`
- `packages/discovery/*`
- `artifacts/endpoint_verification/*`
- `tests/test_discovery_search.py`
- `tests/test_live_1.py`
- `docs/player_pain_discovery.md`
- `docs/current_state.md`
- `.piko/summaries/worker_LIVE-2-R03.md`
- `.piko/summaries/worker_LIVE-2.md`
- `.piko/round_status.json`

禁止修改:

- 不要发布、部署、commit、push。
- 不要 crawler、scrape HTML 或保存 raw/full source。
- 不要下载/生成图片。
- 不要默认调用 LLM 或 translation API。
- 不要绕过 verification 或放宽 Gate。
- 不要把 blocked/skipped 结果显示成 live success。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --live --write-artifact`
- API/window probes for LIVE-2 result surface

完成定义:

- LIVE-2 summaries 存在。
- Operator surface 能显示真实 live 或明确 blocked/failed。
- 若通过验收，必须能证明 `real_collection_performed=true`。
- 没有发布、部署、raw source、crawler、默认 LLM、translation API 或图片副作用。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
