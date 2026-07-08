# Piko-worker Task Prompt: FINISH-1 To FINISH-6

请一次连续执行 FINISH-1 到 FINISH-6，然后停止等待 Piko-verify。目标是把 Piko 收口成一个可实战 MVP：真实外部 approved endpoint 成功时跑通真实采集闭环；没有真实外部 URL 时必须明确 blocked，不允许伪装完成。

## 必读文件

`C:\PycharmProjects\Piko\.piko\round_queue\FINISH-INDEX.md`

## 执行顺序

FINISH-1-R01 -> FINISH-1-R02
FINISH-2-R01 -> FINISH-2-R02
FINISH-3-R01 -> FINISH-3-R02
FINISH-4-R01 -> FINISH-4-R02
FINISH-5-R01 -> FINISH-5-R02
FINISH-6-R01 -> FINISH-6-R02

## 批次目标

把 Piko 变成可插拔、多领域、可真实运行但仍受人类确认控制的 MVP：

- 能验证外部 approved JSON endpoint 的真实成功或正确阻断。
- 能将真实信号进入通用 domain router 和 topic funnel。
- 能生成带证据链的内容包，而不是直接发布。
- 能在 operator console 看到搜索、筛选、证据、内容、发布准备状态。
- 能生成一键发布前的 distribution plan，但默认不上传、不发布、不保存凭据。
- 能输出最终 MVP readiness，明确哪些能力已完成、哪些需要外部账号/endpoint/人工确认。

## 状态要求

如果真实外部 endpoint 可用并通过：

```
current_round=FINISH-1-to-FINISH-6
worker_status=ready_for_verify
verification_status=not_started
last_completed_round=FINISH-6-R02
worker_summary_file=.piko/summaries/worker_FINISH-1-to-FINISH-6.md
next_round=null
```

如果缺少真实外部 endpoint：

```
current_round=FINISH-1-to-FINISH-6
worker_status=blocked_for_external_endpoint
verification_status=not_started
last_completed_round=FINISH-1-R02
worker_summary_file=.piko/summaries/worker_FINISH-1-to-FINISH-6.md
next_round=FINISH-1-R01
```

不要继续生成伪 real artifacts。

## 必须运行的验证

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- FINISH 专项测试，如不存在则新增并运行。
- `python -m packages.workflows.article_pipeline`
- external endpoint / final MVP pipeline CLI，如不存在则新增并运行。
- API/window probes：operator console、final readiness、publish/distribution plan。

## 输出格式

最终 summary 必须包含：

- 修改了什么
- 每个 FINISH stage 和 round 状态
- 外部 endpoint 是否真实成功
- 真实采集结果或 blocked 原因
- 选题漏斗结果
- 内容包结果
- 发布/分发 readiness
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一步建议

