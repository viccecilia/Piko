# Piko-verify Task Prompt: Verify REV-3 To REV-6 Continuous Batch

你是 Piko-verify。请验证 Piko-worker 是否完整执行 REV-3 到 REV-6 连续批处理。不要只验证某一个 Stage；本次目标是总体验收 REV-3-to-REV-6。

验证前提:

- REV-2 已验证通过。
- Worker 应该已经执行：

```text
REV-3-R01 -> REV-3-R02 -> REV-3-R03
REV-4-R01 -> REV-4-R02 -> REV-4-R03
REV-5-R01 -> REV-5-R02 -> REV-5-R03
REV-6-R01 -> REV-6-R02 -> REV-6-R03
```

必须检查的 summary:

- `.piko/summaries/worker_REV-3-R01.md`
- `.piko/summaries/worker_REV-3-R02.md`
- `.piko/summaries/worker_REV-3-R03.md`
- `.piko/summaries/worker_REV-3.md`
- `.piko/summaries/worker_REV-4-R01.md`
- `.piko/summaries/worker_REV-4-R02.md`
- `.piko/summaries/worker_REV-4-R03.md`
- `.piko/summaries/worker_REV-4.md`
- `.piko/summaries/worker_REV-5-R01.md`
- `.piko/summaries/worker_REV-5-R02.md`
- `.piko/summaries/worker_REV-5-R03.md`
- `.piko/summaries/worker_REV-5.md`
- `.piko/summaries/worker_REV-6-R01.md`
- `.piko/summaries/worker_REV-6-R02.md`
- `.piko/summaries/worker_REV-6-R03.md`
- `.piko/summaries/worker_REV-6.md`
- `.piko/summaries/worker_REV-3-to-REV-6.md`

必须运行的验证:

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --fixture`
- `python -m packages.discovery.real_endpoint_verify --fixture --write-artifact`
- `python -m packages.discovery.real_endpoint_verify --live`
- `python -m packages.workflows.article_pipeline`
- API probes:
  - `/discovery/funnel-window`
  - `/discovery/funnel-trace`
  - `/discovery/rankings`
  - `/discovery/search`
  - final result/publish-readiness surface if added by worker

核心验收点:

- REV-3 Real Search Endpoint Setup:
  - Approved source registry 存在。
  - Steam / Reddit / SERP / JP / KR endpoint category 可配置。
  - 默认不触网。
  - live 需要 opt-in 和 approved endpoint URL。
  - HTML/raw body/未知 source category 被拒绝或 unsupported。
  - source-level trace/artifact/window 能显示 requested source、normalized count、discarded count、skip reason、mode、real_collection_performed。

- REV-4 Real Hot Game And Question Discovery:
  - Endpoint-fed hot game Top 5 / Top 20 可输出。
  - Endpoint-fed hot player questions 可进入 buckets：已有答案、未解决高热、冲突答案、高风险阻断、必须查攻略。
  - API/window 可见当前最热游戏、棘手问题、已有答案/未解决/冲突/高风险栏目。
  - fixture/mock-live/real-source 模式如实显示。

- REV-5 Real Funnel Candidate Probe:
  - Safe publish_candidate 可被选为 internal candidate。
  - watchlist/high-risk 不进入 normal draft。
  - conflict topic 不伪装成确定解决方案。
  - latest funnel report artifact 存在，可回答：热游、问题、解决方案线索、候选选择、阻断原因、mode、source trace。
  - report 中 `publish_ready=false`、`publishing_performed=false`。

- REV-6 Article Package And Publish-Readiness Surface:
  - Safe candidate 能进入 SourceAgent -> EvidenceAgent -> RankingAgent -> WriterAgent -> EditorAgent -> FactcheckAgent -> VerificationGate，或在证据不足时安全阻断。
  - Article package 保留 source_ids、evidence_card_ids、claim_trace、ranked_steps。
  - Media plan 存在：recommended_media、required_screenshots、image_source_policy、alt_text、license/safety notes。
  - 如果没图，应明确 `has_images=false` 且 `media_plan_present=true`。
  - Publish readiness metadata 存在，但不能等于真正发布。
  - 本地窗口/API 显示：
    - 当前最热游戏
    - 棘手玩家问题
    - 已搜索到的解决方案线索
    - 已生成文章包
    - 配图/媒体计划
    - 发布准备状态

安全禁止项扫描:

- 不得发现 crawler。
- 不得发现 HTML scrape 作为默认路径。
- 不得保存 raw response body、raw_text、body、selftext、content、full_comments、raw_page_text、full posts/pages/comments、credentials、secrets、api_key、authorization。
- 不得发布、deploy、commit、push。
- 不得默认调用 LLM、translation API、image generation。
- 不得绕过 verification 或放宽 Gate。
- 不得伪装 skipped/mock-live 为真实采集。
- 不得下载外部图片。

round_status 期望:

- `worker_status=ready_for_verify`
- `verification_status=not_started`
- `last_completed_round=REV-6-R03`
- `last_verified_round=REV-2`
- `worker_summary_file=.piko/summaries/worker_REV-3-to-REV-6.md`
- `next_round=null`

通过后请更新:

- 生成 `.piko/summaries/verify_REV-3-to-REV-6.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=REV-3-to-REV-6`
  - `verification_summary_file=.piko/summaries/verify_REV-3-to-REV-6.md`
  - `next_round=null`
  - UTF-8 no BOM

失败时请更新:

- `worker_status=needs_fix`
- `verification_status=failed`
- `next_round=REV-3-to-REV-6`
- 写明阻断问题和精确返工任务。

输出格式:

- 验证结论
- 已生成验证报告
- 已运行验证
- Stage 完整性检查
- REV-3 检查结果
- REV-4 检查结果
- REV-5 检查结果
- REV-6 检查结果
- API / artifact / window 检查
- guardrail 检查
- 发现的问题
- 建议返工任务
