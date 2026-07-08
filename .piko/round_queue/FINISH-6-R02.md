# Round ID: FINISH-6-R02
Round Name: Final FINISH Verification Prep

本轮目标:

完成 FINISH-1 到 FINISH-6 最终自检，写总 summary，更新 round_status，并停止等待 Piko-verify。

本轮任务:
- 执行任务:
  - 汇总所有 FINISH artifacts、round summaries、stage summaries。
  - 运行全量验证。
  - 生成 `.piko/summaries/worker_FINISH-6-R02.md`
  - 生成 `.piko/summaries/worker_FINISH-6.md`
  - 生成 `.piko/summaries/worker_FINISH-1-to-FINISH-6.md`
  - 更新 `.piko/round_status.json`。
- 测试任务:
  - 运行 full pytest。
  - 运行 FINISH 专项测试。
  - 运行 article pipeline smoke。
  - 运行 API/window probes。
- 协作验收任务:
  - 明确告诉 Piko-verify：这是 final MVP closure 验收，不是单 stage 验收。

允许修改:

- `.piko/summaries/**`
- `.piko/round_status.json`
- `artifacts/final_mvp/**`
- `docs/**`
- 必要测试与 pipeline 文件

禁止修改:

- 不得进入其它队列。
- 不得发布、上传、部署、commit/push。
- 不得绕过任何失败测试。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- FINISH 专项测试
- `python -m packages.workflows.article_pipeline`
- final MVP CLI/API/window probes

完成定义:

- FINISH 批次可以交给 Piko-verify。
- 如果 external success 存在，证据完整。
- 如果 external endpoint 缺失，blocked 诚实完整。
- Piko MVP readiness 状态没有夸大。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

