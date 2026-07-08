# Piko-verify Task Prompt: Verify FINISH-1 To FINISH-6

请一次性验证 FINISH-1 到 FINISH-6 连续批次。重点不是“代码有没有写”，而是 Piko 是否已经形成可实战 MVP 闭环，且没有伪装真实数据或绕过人类确认。

## 验证入口

`C:\PycharmProjects\Piko\.piko\summaries\worker_FINISH-1-to-FINISH-6.md`

## 必验顺序

FINISH-1-R01 -> FINISH-1-R02
FINISH-2-R01 -> FINISH-2-R02
FINISH-3-R01 -> FINISH-3-R02
FINISH-4-R01 -> FINISH-4-R02
FINISH-5-R01 -> FINISH-5-R02
FINISH-6-R01 -> FINISH-6-R02

## 必验命令

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- FINISH 专项测试
- `python -m packages.workflows.article_pipeline`
- final MVP / external endpoint CLI probe
- API probes for final readiness, operator console, publish/distribution plan

## 通过条件

如果配置了真实外部 approved endpoint：

- 必须证明 non-local HTTP(S) endpoint 被 fetch。
- 必须证明 endpoint contract validation passed。
- 必须证明 `real_collection_performed=true`。
- scope 必须是 `external_approved_endpoint` 或更具体的 approved external provider，不得是 local/fixture/mock。
- 真实信号必须进入 domain router、topic funnel、content package、operator console。
- publish/distribution 必须仍停在 human approval gate 前。

如果没有配置真实外部 approved endpoint：

- 可以通过为“正确安全阻断”，但必须是 `blocked_for_external_endpoint`。
- 不得生成伪造的 real success。
- 不得把 local endpoint、fixture、mock-live、静态包标记成 external success。
- 必须输出清晰的 operator run instructions。

## Guardrail 必查

- 无 crawler
- 无 HTML scrape
- 无 raw/full source 保存
- 无 credentials/secrets 保存
- 无默认联网
- 无默认 LLM
- 无发布、上传、部署
- 无 auto install / auto replace active skill/domain/connector/runtime
- 无 verification bypass
- 无 Gate 放宽

## 验收输出

生成 `.piko/summaries/verify_FINISH-1-to-FINISH-6.md`。

通过时更新：

```
worker_status=complete
verification_status=passed
last_verified_round=FINISH-1-to-FINISH-6
verification_summary_file=.piko/summaries/verify_FINISH-1-to-FINISH-6.md
next_round=null
```

若真实 endpoint 缺失但阻断正确，也可 passed，但必须在结论中写明“不是 external live success，只是正确安全阻断”。

失败时更新：

```
worker_status=needs_fix
verification_status=failed
next_round=FINISH-1-to-FINISH-6
```

