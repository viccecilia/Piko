# Piko-verify Task Prompt: Verify SOURCE-PROVIDER-1 To SOURCE-PROVIDER-5

请一次性验证 SOURCE-PROVIDER-1 到 SOURCE-PROVIDER-5 连续批次。重点确认是否真的准备了外部 approved JSON endpoint provider；如果没有真实外部 URL，则必须明确 blocked/deploy-ready，不能伪装 external success。

入口 summary：

`C:\PycharmProjects\Piko\.piko\summaries\worker_SOURCE-PROVIDER-1-to-SOURCE-PROVIDER-5.md`

验证范围：

```text
SOURCE-PROVIDER-1-R01 -> SOURCE-PROVIDER-1-R02
SOURCE-PROVIDER-2-R01 -> SOURCE-PROVIDER-2-R02 -> SOURCE-PROVIDER-2-R03
SOURCE-PROVIDER-3-R01 -> SOURCE-PROVIDER-3-R02
SOURCE-PROVIDER-4-R01 -> SOURCE-PROVIDER-4-R02
SOURCE-PROVIDER-5-R01 -> SOURCE-PROVIDER-5-R02
```

必须检查：

- 所有 SOURCE-PROVIDER round summary 存在。
- 所有 SOURCE-PROVIDER stage summary 存在。
- final summary `.piko/summaries/worker_SOURCE-PROVIDER-1-to-SOURCE-PROVIDER-5.md` 存在。
- `round_status.json` 是 UTF-8 no BOM 且合法 JSON。
- worker 状态应为 `ready_for_verify`。

必须检查 artifacts：

- Provider strategy artifact
- Approved endpoint payload artifact
- Static endpoint package artifact
- External URL validation artifact
- Piko env handoff artifact
- Operator instruction artifact

必须运行的验证：

- `python -c "import json; json.load(open('.piko/round_status.json', encoding='utf-8')); print('round_status json ok')"`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- SOURCE-PROVIDER专项测试
- Provider artifacts JSON parse probes
- External URL validation or blocked status probe
- Guardrail scan

核心验收点：

- localhost/file/fixture 不得被标记为 external success。
- 如果有外部 URL，必须 fetch 并通过 approved endpoint contract validation。
- 如果没有外部 URL，必须输出 deploy_ready_pending_host 或 blocked_for_external_url。
- 不得保存凭据或远程平台 token。
- 输出必须包含后续 EXTERNAL-ENDPOINT env 指令。

安全禁止项：

- 不得保存 token/cookie/API key/authorization/credentials。
- 不得 crawler 或 scrape HTML。
- 不得发布文章、社交内容或部署远程站点，除非有明确批准且本轮要求允许。
- 不得默认调用 LLM。
- 不得绕过 verification 或放宽 Gate。

通过时：

- 生成 `.piko/summaries/verify_SOURCE-PROVIDER-1-to-SOURCE-PROVIDER-5.md`
- 更新 `.piko/round_status.json`：
  - `worker_status=complete`
  - `verification_status=passed`
  - `last_verified_round=SOURCE-PROVIDER-1-to-SOURCE-PROVIDER-5`
  - `verification_summary_file=.piko/summaries/verify_SOURCE-PROVIDER-1-to-SOURCE-PROVIDER-5.md`
  - `next_round=null`

失败时：

- 生成失败验证报告。
- 更新 `.piko/round_status.json`：
  - `worker_status=needs_fix`
  - `verification_status=failed`
  - `next_round=SOURCE-PROVIDER-1-to-SOURCE-PROVIDER-5`

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- SOURCE-PROVIDER-1 检查结果
- SOURCE-PROVIDER-2 检查结果
- SOURCE-PROVIDER-3 检查结果
- SOURCE-PROVIDER-4 检查结果
- SOURCE-PROVIDER-5 检查结果
- provider validated/blocked 状态
- API / artifact 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
