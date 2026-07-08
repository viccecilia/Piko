# Piko-verify Task Prompt: Verify REALDATA-1 To REALDATA-6

请一次性验证 REALDATA-1 到 REALDATA-6 连续批次。本轮不是验证单个 approved endpoint，而是验证 Piko 是否具备多真实 provider 摘要 endpoint 的受控接入能力。

## 验证入口

`C:\PycharmProjects\Piko\.piko\summaries\worker_REALDATA-1-to-REALDATA-6.md`

## 必验顺序

REALDATA-1-R01 -> REALDATA-1-R02
REALDATA-2-R01 -> REALDATA-2-R02 -> REALDATA-2-R03
REALDATA-3-R01 -> REALDATA-3-R02
REALDATA-4-R01 -> REALDATA-4-R02
REALDATA-5-R01 -> REALDATA-5-R02
REALDATA-6-R01 -> REALDATA-6-R02

## 必验命令

- REALDATA 专项测试
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- `python -m packages.workflows.article_pipeline`
- REALDATA pipeline CLI
- REALDATA API/window probes
- structured artifact scan

## 通过条件

如果 provider endpoints 配置完整或部分配置：

- 必须证明每个 configured provider 是 HTTP(S) approved JSON endpoint。
- 必须证明真实请求发生于 configured provider endpoint。
- 必须证明 retained fields bounded。
- 必须证明 raw/full source fields 没有保存。
- 至少一个 provider 成功时可 `real_collection_performed=true`，但 coverage 必须明确是 partial 或 listed provider coverage。
- 多 provider 成功时必须列出每个 provider 的 counts、freshness、source trace。
- 真实信号必须进入 topic funnel、content package、operator surface。

如果没有 provider endpoints：

- 可以通过为“正确安全阻断”，但必须是 `blocked_for_provider_endpoints`。
- 不得用 FINISH 的 `paste.rs` single endpoint、fixture、local endpoint 或 mock-live 冒充 multi-provider success。
- 必须输出清楚的 env run instructions。

## Guardrail 必查

- 无 crawler。
- 无 HTML scrape。
- 无 raw/full source 保存。
- 无 credentials/secrets 保存。
- 无默认联网。
- 无默认 LLM。
- 无发布、上传、部署。
- 无 broad internet coverage 夸大。
- 无 verification bypass 或 Gate 放宽。

## 验收输出

生成 `.piko/summaries/verify_REALDATA-1-to-REALDATA-6.md`。

通过时更新：

```
worker_status=complete
verification_status=passed
last_verified_round=REALDATA-1-to-REALDATA-6
verification_summary_file=.piko/summaries/verify_REALDATA-1-to-REALDATA-6.md
next_round=null
```

失败时更新：

```
worker_status=needs_fix
verification_status=failed
next_round=REALDATA-1-to-REALDATA-6
```

