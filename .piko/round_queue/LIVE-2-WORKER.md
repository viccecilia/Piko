# Piko-worker Task Prompt: LIVE-2 Real Approved Endpoint Verification

你是 Piko-worker。LIVE-1 已验证通过，但那是 safe skipped，不是真实联网。现在执行 LIVE-2，目标是连接真实 approved JSON endpoint，并证明 `real_collection_performed=true`。

执行范围:

```text
LIVE-2-R01 -> LIVE-2-R02 -> LIVE-2-R03
```

执行前必须确认:

```powershell
$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE="true"
$env:PIKO_LIVE_DISCOVERY_TEST="true"
$env:PIKO_APPROVED_ENDPOINT_URL="https://<approved-json-endpoint>"
```

如果 `PIKO_APPROVED_ENDPOINT_URL` 没有配置:

- 不要继续伪装真实 live。
- 写清楚 blocked reason。
- `worker_status` 可以设为 `blocked_for_endpoint`。
- `next_round=LIVE-2-R01`。
- 告诉 operator 需要提供 approved JSON endpoint URL。

执行方法:

1. 阅读 `.piko/round_queue/LIVE-2-INDEX.md`。
2. 按顺序执行：
   - `.piko/round_queue/LIVE-2-R01.md`
   - `.piko/round_queue/LIVE-2-R02.md`
   - `.piko/round_queue/LIVE-2-R03.md`
3. 每完成一个 round，写：
   - `.piko/summaries/worker_LIVE-2-R01.md`
   - `.piko/summaries/worker_LIVE-2-R02.md`
   - `.piko/summaries/worker_LIVE-2-R03.md`
4. 完成或阻塞后写：
   - `.piko/summaries/worker_LIVE-2.md`

成功 ready_for_verify 条件:

- endpoint 已配置。
- live request 实际发生。
- approved endpoint contract 通过。
- artifact 显示 `mode=real-source`。
- artifact 显示 `real_collection_performed=true`。
- normalized game/question counts 大于 0 或有明确可接受的 live-empty reason。
- 未保存 raw/full source。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest tests\test_live_1.py -q`
- `python -m pytest`
- `python -m packages.discovery.real_endpoint_verify --live --write-artifact`
- API/window probes for LIVE-2 result surface.

禁止项:

- 不要 crawler。
- 不要 scrape HTML。
- 不要保存 raw response body、full source payload、full posts/pages/comments、credentials、secrets、api_key、authorization。
- 不要发布、部署、commit、push。
- 不要默认调用 LLM、translation API、image generation。
- 不要绕过 verification 或放宽 Gate。
- 不要把 blocked/skipped/fallback 写成 real live success。

最终输出格式:

- 修改了什么
- LIVE-2-R01 状态
- LIVE-2-R02 状态
- LIVE-2-R03 状态
- Endpoint URL 是否配置
- 是否真实联网
- `real_collection_performed` 值
- normalized games/questions 数量
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
