# Piko-worker Task Prompt: SOURCE-PROVIDER-1 To SOURCE-PROVIDER-5

请一次连续执行 SOURCE-PROVIDER-1 到 SOURCE-PROVIDER-5，然后停止等待 Piko-verify。

请先读取：

`C:\PycharmProjects\Piko\.piko\round_queue\SOURCE-PROVIDER-INDEX.md`

执行顺序：

```text
SOURCE-PROVIDER-1-R01 -> SOURCE-PROVIDER-1-R02
SOURCE-PROVIDER-2-R01 -> SOURCE-PROVIDER-2-R02 -> SOURCE-PROVIDER-2-R03
SOURCE-PROVIDER-3-R01 -> SOURCE-PROVIDER-3-R02
SOURCE-PROVIDER-4-R01 -> SOURCE-PROVIDER-4-R02
SOURCE-PROVIDER-5-R01 -> SOURCE-PROVIDER-5-R02
```

本批次目标：

- 准备一个真正外部可访问的 approved JSON endpoint provider。
- 生成符合 Piko approved endpoint contract 的 JSON payload。
- 生成外部静态 endpoint 发布包。
- 如果有已批准外部 URL，则验证该 URL；如果没有，则输出 deploy_ready_blocked，不伪装 external success。
- 生成后续 EXTERNAL-ENDPOINT 重跑所需的 env/config 指令。

硬边界：

- localhost、file、fixture、127.0.0.1 都不算 external endpoint。
- 没有外部 URL 时，状态必须是 blocked_for_external_url 或 deploy_ready_pending_host。
- 只有非本地 HTTP(S) URL 被 fetch 且 contract validation 通过，才允许 external_provider_validated=true。

全局禁止项：

- 不保存 token/cookie/API key/authorization/credentials。
- 不自动上传到远程平台，除非已有明确 operator approval 和安全凭据通道。
- 不 crawler。
- 不 scrape HTML。
- 不发布文章或社交内容。
- 不默认调用 LLM。
- 不绕过 verification，不放宽 Gate。

必须运行的验证：

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- SOURCE-PROVIDER 专项测试
- Provider artifacts JSON parse probes
- External URL validation or blocked status probe
- Guardrail scan

最终更新 `.piko/round_status.json`：

```text
current_round=SOURCE-PROVIDER-1-to-SOURCE-PROVIDER-5
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=SOURCE-PROVIDER-5-R02
worker_summary_file=.piko/summaries/worker_SOURCE-PROVIDER-1-to-SOURCE-PROVIDER-5.md
next_round=null
```

最终输出格式：

- 修改了什么
- SOURCE-PROVIDER-1 每个 round 状态
- SOURCE-PROVIDER-2 每个 round 状态
- SOURCE-PROVIDER-3 每个 round 状态
- SOURCE-PROVIDER-4 每个 round 状态
- SOURCE-PROVIDER-5 每个 round 状态
- provider 状态：validated_external_url / deploy_ready_pending_host / blocked_for_external_url / needs_fix
- external URL 或待部署包路径
- 下一步 EXTERNAL-ENDPOINT env 指令
- 生成的 artifacts
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
