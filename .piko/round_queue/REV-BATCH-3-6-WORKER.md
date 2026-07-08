# Piko-worker Task Prompt: REV-3 To REV-6 Continuous Batch

你是 Piko-worker。REV-2 已由 Piko-verify 验证通过。现在请连续执行 `.piko/round_queue` 中 REV-3 到 REV-6 的所有 rounds，不要每个 Stage 停下来等验证。

执行范围:

```text
REV-3-R01 -> REV-3-R02 -> REV-3-R03
REV-4-R01 -> REV-4-R02 -> REV-4-R03
REV-5-R01 -> REV-5-R02 -> REV-5-R03
REV-6-R01 -> REV-6-R02 -> REV-6-R03
```

执行方法:

1. 先阅读 `.piko/round_queue/REV-INDEX.md`。
2. 按顺序读取并执行每个 round 文件。
3. 每完成一个 round，写一个 summary：
   - `.piko/summaries/worker_REV-3-R01.md`
   - ...
   - `.piko/summaries/worker_REV-6-R03.md`
4. 每完成一个 Stage，写一个 stage summary：
   - `.piko/summaries/worker_REV-3.md`
   - `.piko/summaries/worker_REV-4.md`
   - `.piko/summaries/worker_REV-5.md`
   - `.piko/summaries/worker_REV-6.md`
5. REV-6-R03 完成后，写最终 batch summary：
   - `.piko/summaries/worker_REV-3-to-REV-6.md`
6. 最后更新 `.piko/round_status.json`：
   - `current_round=REV-3-to-REV-6`
   - `worker_status=ready_for_verify`
   - `verification_status=not_started`
   - `last_completed_round=REV-6-R03`
   - `last_verified_round=REV-2`
   - `worker_summary_file=.piko/summaries/worker_REV-3-to-REV-6.md`
   - `next_round=null`
   - 文件必须是 UTF-8 no BOM、合法 JSON。

本批目标:

- 接入 approved JSON endpoint registry。
- 实现受控 real search endpoint adapter。
- 展示 endpoint source trace。
- 输出 endpoint-fed 热门游戏排行。
- 输出 endpoint-fed 玩家棘手问题排行。
- 从漏斗中选择安全文章候选。
- 生成 solution hints / evidence readiness。
- 生成 latest real market funnel report。
- 生成 internal source-backed article package 或安全阻断报告。
- 增加 media plan / publish readiness metadata。
- 在本地窗口/API 展示：
  - 当前最热游戏
  - 棘手玩家问题
  - 已搜索到的解决方案线索
  - 已生成文章包
  - 配图/媒体计划
  - 发布准备状态

全局禁止项:

- 不要默认触网。
- 真实采集必须显式 opt-in 且使用 approved JSON endpoint。
- 不要 crawler。
- 不要 scrape HTML。
- 不要保存 full posts、full pages、full comments、raw response bodies、images、maps、copied tables、credentials、API keys、authorization headers、secrets。
- 不要发布、部署、commit、push。
- 不要默认调用 LLM、translation API 或 image generation。
- 不要绕过 verification 或放宽 Gate。
- 不要伪装 skipped/mock-live 为真实采集。
- 不要删除旧 artifacts 来逃避测试。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --fixture`
- `python -m packages.discovery.real_endpoint_verify --fixture --write-artifact`
- `python -m packages.discovery.real_endpoint_verify --live`
- `python -m packages.workflows.article_pipeline`
- API/window probes for:
  - `/discovery/funnel-window`
  - `/discovery/funnel-trace`
  - `/discovery/rankings`
  - `/discovery/search`
  - final result/publish-readiness surface

最终输出格式:

- 修改了什么
- REV-3 每个 round 状态
- REV-4 每个 round 状态
- REV-5 每个 round 状态
- REV-6 每个 round 状态
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
