# Round ID: PROVIDER-LIVE-5-R02
Round Name: Final PROVIDER-LIVE Verification Prep

本轮目标:

完成 PROVIDER-LIVE 批次最终自检，写 summary，更新状态并停止等待 Piko-verify。

本轮任务:
- 执行任务:
  - 汇总所有 provider artifacts、round summaries、stage summaries。
  - 生成 `.piko/summaries/worker_PROVIDER-LIVE-5-R02.md`
  - 生成 `.piko/summaries/worker_PROVIDER-LIVE-5.md`
  - 生成 `.piko/summaries/worker_PROVIDER-LIVE-1-to-PROVIDER-LIVE-5.md`
  - 更新 `.piko/round_status.json`。
- 测试任务:
  - 运行 full pytest。
  - 运行 PROVIDER-LIVE 专项测试。
  - 运行 REALDATA 专项测试。
  - 运行 provider endpoint validation probe。
  - 运行 structured guardrail scan。
- 协作验收任务:
  - 明确告诉 Piko-verify：这是 REALDATA provider endpoint 准备批次，不是 REALDATA partial coverage 验收。

允许修改:

- `.piko/summaries/**`
- `.piko/round_status.json`
- `artifacts/provider_live/**`
- 必要代码、测试、文档

禁止修改:

- 不得进入 REALDATA 重跑，除非任务明确要求 smoke；即便 smoke，也不能更新 REALDATA 验收状态。
- 不得发布、上传、部署、commit/push。

必须运行的验证:

- `python -m pytest tests\test_realdata_pipeline.py -q`
- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- PROVIDER-LIVE 专项测试

完成定义:

- PROVIDER-LIVE 批次可交给 Piko-verify。
- 至少 deploy-ready；若 endpoint 成功，则 partial provider endpoint ready。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

