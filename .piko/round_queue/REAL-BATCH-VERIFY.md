# Piko-verify Task Prompt: Verify REAL-1 To REAL-5 Real Data Market Pilot

请一次性验证 REAL-1 到 REAL-5 连续批次。通过条件取决于真实环境：如果 endpoint 配置完整，必须验证真实采集和真实 artifact；如果 endpoint 缺失，正确 blocked_for_endpoint 也可以作为安全通过，但不能声称已有真实市场覆盖。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_REAL-1-to-REAL-5.md`

验证范围：

```text
REAL-1-R01 -> REAL-1-R02
REAL-2-R01 -> REAL-2-R02 -> REAL-2-R03
REAL-3-R01 -> REAL-3-R02 -> REAL-3-R03
REAL-4-R01 -> REAL-4-R02
REAL-5-R01 -> REAL-5-R02
```

必须检查：

- 所有已执行 REAL round summary 存在。
- 所有已执行 REAL stage summary 存在。
- final summary `.piko/summaries/worker_REAL-1-to-REAL-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- 如果未配置 endpoint，状态应为 `worker_status=blocked_for_endpoint`。
- 如果配置 endpoint 并完成全批次，状态应为 `worker_status=ready_for_verify`、`last_completed_round=REAL-5-R02`。

必须检查 artifacts：

- Live data readiness artifact
- Endpoint verification artifact
- Real collection normalized signals artifact
- Live ranking/funnel artifact
- Topic selection artifact
- Source-backed article package artifact
- Publish readiness artifact
- Operator result artifact

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- Real endpoint live/blocked verification
- Real collection artifact JSON parse probes
- Funnel/ranking artifact probes
- Article package safety probes
- API/window probes if implemented
- Guardrail scan

核心验收点：

- 真实采集需要明确 opt-in 和 approved endpoint。
- `real_collection_performed=true` 必须有 endpoint verification evidence。
- 缺 endpoint 时不得声称实时数据成功。
- 热门游戏 Top 5 / Top 20 和 pain buckets 必须来自 normalized signals 或明确标记 fixture/blocked。
- Candidate article package 必须 source/evidence trace 完整，publish_ready=false，publishing_performed=false。
- Watchlist/high-risk 不得进入 normal publish candidate。

安全禁止项：

- 不得 crawler。
- 不得 scrape HTML。
- 不得保存 raw response body、full posts、full comments、full pages、images、maps、tables。
- 不得保存 secrets、credentials、authorization、API key。
- 不得默认调用 LLM。
- 不得发布、部署、commit、push。
- 不得绕过 verification 或放宽 Gate。

通过时：

- 生成 `.piko/summaries/verify_REAL-1-to-REAL-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete` 或保留安全 blocked 状态并写明原因
  - `verification_status=passed`
  - `last_verified_round=REAL-1-to-REAL-5`
  - `verification_summary_file=.piko/summaries/verify_REAL-1-to-REAL-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=REAL-1-to-REAL-5`

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- REAL-1 检查结果
- REAL-2 检查结果
- REAL-3 检查结果
- REAL-4 检查结果
- REAL-5 检查结果
- 真实采集 success/blocked 状态
- Top 5 / pain buckets / article package 检查
- API / artifact / window 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
