# Round ID: REALDATA-6-R02
Round Name: Final REALDATA Verification Prep

本轮目标:

完成 REALDATA-1 到 REALDATA-6 最终自检，写总 summary，更新状态并停止等待 Piko-verify。

本轮任务:
- 执行任务:
  - 汇总所有 REALDATA artifacts、round summaries、stage summaries。
  - 生成 `.piko/summaries/worker_REALDATA-6-R02.md`
  - 生成 `.piko/summaries/worker_REALDATA-6.md`
  - 生成 `.piko/summaries/worker_REALDATA-1-to-REALDATA-6.md`
  - 更新 `.piko/round_status.json`。
- 测试任务:
  - 运行 full pytest。
  - 运行 REALDATA 专项测试。
  - 运行 article pipeline smoke。
  - 运行 API/window probes。
  - 运行 structured guardrail scan。
- 协作验收任务:
  - 明确告诉 Piko-verify：这是多真实 provider 数据源生产化验收，不是 FINISH 单 endpoint 验收。

允许修改:

- `.piko/summaries/**`
- `.piko/round_status.json`
- `artifacts/realdata/**`
- 必要代码、测试、文档

禁止修改:

- 不得进入其它队列。
- 不得发布、上传、部署、commit/push。
- 不得绕过测试失败。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- REALDATA 专项测试
- `python -m packages.workflows.article_pipeline`
- REALDATA CLI/API/window probes

完成定义:

- REALDATA 批次可以交给 Piko-verify。
- 若 provider endpoint 缺失，blocked 诚实完整。
- 若 provider endpoint 成功，真实采集和漏斗链路证据完整。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

