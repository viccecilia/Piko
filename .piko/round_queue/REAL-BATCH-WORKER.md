# Piko-worker Task Prompt: REAL-1 To REAL-5 Real Data Market Pilot

请一次连续执行 REAL-1 到 REAL-5，然后停止等待 Piko-verify。目标是进入真实数据：用 approved JSON endpoint 或批准的真实来源配置，收集当前热门游戏和玩家痛点，完成漏斗排行，生成内部候选文章包。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\REAL-INDEX.md`

执行顺序：

```text
REAL-1-R01 -> REAL-1-R02
REAL-2-R01 -> REAL-2-R02 -> REAL-2-R03
REAL-3-R01 -> REAL-3-R02 -> REAL-3-R03
REAL-4-R01 -> REAL-4-R02
REAL-5-R01 -> REAL-5-R02
```

本批次目标：

- 检查 approved live data env/config。
- 如果配置完整，执行真实 approved endpoint verification。
- 将真实 payload normalize 为 hot games / player questions。
- 输出当前热门游戏 Top 5 / Top 20。
- 输出高热痛点 buckets：已有答案、未解决监控、冲突答案、高风险阻断、必须查攻略。
- 选择一个 safe publish_candidate，生成 source-backed internal article package。
- 仍然不发布，只到一键发布前候选状态。

硬门槛：

- 没有 `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`、`PIKO_LIVE_DISCOVERY_TEST=true`、approved endpoint URL，就必须 `blocked_for_endpoint`。
- endpoint contract 不通过，就必须 `failed_contract_validation`。
- 真实采集成功才允许 `real_collection_performed=true`。
- 不得伪装 live success。

全局禁止项：

- 不 crawler。
- 不 scrape HTML。
- 不保存 raw response body / full posts / full pages / full comments。
- 不保存 secrets、credentials、authorization、API key。
- 不默认调用 LLM。
- 不发布、不部署、不 commit、不 push。
- 不自动发布文章。
- 不绕过 verification，不放宽 Gate。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- Real endpoint live/blocked verification
- Real collection artifact JSON parse probes
- Funnel/ranking artifact probes
- Article package safety probes
- API/window probes if implemented
- Guardrail scan

最终更新 `.piko/round_status.json`：

```text
current_round=REAL-1-to-REAL-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=REAL-5-R02
worker_summary_file=.piko/summaries/worker_REAL-1-to-REAL-5.md
next_round=null
```

如果 endpoint 缺失：

```text
current_round=REAL-1-to-REAL-5
worker_status=blocked_for_endpoint
verification_status=not_started
last_completed_round=REAL-1-R02
worker_summary_file=.piko/summaries/worker_REAL-1-to-REAL-5.md
next_round=REAL-1-R01
```

最终输出格式：

- 修改了什么
- REAL-1 每个 round 状态
- REAL-2 每个 round 状态
- REAL-3 每个 round 状态
- REAL-4 每个 round 状态
- REAL-5 每个 round 状态
- 真实采集状态：success / blocked_for_endpoint / failed_contract_validation / needs_fix
- 热门游戏 Top 5
- 高热痛点 buckets
- 候选文章包状态
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
