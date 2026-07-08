# Piko-worker Task Prompt: LIVE-1 Approved Live Endpoint Connection

你是 Piko-worker。REV-3-to-REV-6 已由 Piko-verify 验证通过。现在执行 LIVE-1，用 approved JSON endpoint 做一次小流量真实联网验证；如果当前机器没有配置 endpoint，则必须安全 skipped，并清楚报告缺少什么。

执行范围:

```text
LIVE-1-R01 -> LIVE-1-R02 -> LIVE-1-R03
```

执行方法:

1. 先阅读 `.piko/round_queue/LIVE-INDEX.md`。
2. 按顺序读取并执行：
   - `.piko/round_queue/LIVE-1-R01.md`
   - `.piko/round_queue/LIVE-1-R02.md`
   - `.piko/round_queue/LIVE-1-R03.md`
3. 每完成一个 round，写一个 summary：
   - `.piko/summaries/worker_LIVE-1-R01.md`
   - `.piko/summaries/worker_LIVE-1-R02.md`
   - `.piko/summaries/worker_LIVE-1-R03.md`
4. 完成 LIVE-1 后写 stage summary：
   - `.piko/summaries/worker_LIVE-1.md`
5. 最后更新 `.piko/round_status.json`：
   - `current_round=LIVE-1`
   - `worker_status=ready_for_verify`
   - `verification_status=not_started`
   - `last_completed_round=LIVE-1-R03`
   - `last_verified_round=REV-3-to-REV-6`
   - `worker_summary_file=.piko/summaries/worker_LIVE-1.md`
   - `next_round=null`
   - 文件必须是 UTF-8 no BOM、合法 JSON。

本批目标:

- 检查 approved endpoint 配置 readiness。
- 执行 bounded live endpoint smoke。
- 如果 endpoint 未配置，安全 skipped，不伪装成功。
- 如果 endpoint 已配置且显式 opt-in，真实请求 approved JSON endpoint。
- 生成 endpoint verification artifact。
- 在 operator surface/API 显示 LIVE-1 结果。
- 保持 candidate-only，不发布。

真实联网条件:

只有同时满足以下条件才允许真实联网：

- `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`
- `PIKO_LIVE_DISCOVERY_TEST=true`
- `PIKO_APPROVED_ENDPOINT_URL=<approved-json-endpoint>`

如果缺任一条件：

- 必须输出 `status=skipped`
- 必须输出 `real_collection_performed=false`
- 必须写明 missing configuration
- 不得失败成阻断
- 不得伪装成真实 live success

全局禁止项:

- 不要默认触网。
- 不要 crawler。
- 不要 scrape HTML。
- 不要保存 full posts、full pages、full comments、raw response bodies、images、maps、copied tables、credentials、API keys、authorization headers、secrets。
- 不要发布、部署、commit、push。
- 不要默认调用 LLM、translation API 或 image generation。
- 不要绕过 verification 或放宽 Gate。
- 不要删除旧 artifacts 来逃避测试。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --fixture`
- `python -m packages.discovery.real_endpoint_verify --fixture --write-artifact`
- `python -m packages.discovery.real_endpoint_verify --live`
- 如果 endpoint env vars 已配置，运行显式 opt-in live verification，并记录 `real_collection_performed`。
- API/window probes for LIVE-1 result surface.

最终输出格式:

- 修改了什么
- LIVE-1-R01 状态
- LIVE-1-R02 状态
- LIVE-1-R03 状态
- Endpoint 配置状态
- 是否真实联网
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
