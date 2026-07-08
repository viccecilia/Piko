# Round ID: ENDPOINT-5-R02

Round Name: Final ENDPOINT Verification Prep

本轮目标:

完成 ENDPOINT 批次最终验证准备，跑全量验证，写最终 worker summary，并停止等待 Piko-verify。

本轮任务:
- 执行任务:
  - 汇总 ENDPOINT-1 到 ENDPOINT-5 所有 artifacts 和 summaries。
  - 更新 docs/current_state 或相关文档，说明 local approved endpoint success path 和 broad internet coverage 的区别。
  - 更新 `.piko/round_status.json` 为 ready_for_verify。
- 测试任务:
  - 运行 `python -m pytest tests\test_discovery_search.py -q`
  - 运行 `python -m pytest`
  - 运行 ENDPOINT 专项测试。
  - 运行 artifact JSON parse probes。
  - 运行 guardrail scan。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_ENDPOINT-5-R02.md`
  - 生成 `.piko/summaries/worker_ENDPOINT-5.md`
  - 生成 `.piko/summaries/worker_ENDPOINT-1-to-ENDPOINT-5.md`

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/local_endpoint/*`
- `.piko/summaries/worker_ENDPOINT-5-R02.md`
- `.piko/summaries/worker_ENDPOINT-5.md`
- `.piko/summaries/worker_ENDPOINT-1-to-ENDPOINT-5.md`
- `.piko/round_status.json`

禁止修改:

- 不进入下一批次。
- 不发布、不部署。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- ENDPOINT 专项测试
- Artifact JSON parse probes
- Guardrail scan

完成定义:

- ENDPOINT 全批次可交给 Piko-verify。
- local approved endpoint success path 已证明且边界清楚。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
