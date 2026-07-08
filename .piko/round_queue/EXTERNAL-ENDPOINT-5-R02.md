# Round ID: EXTERNAL-ENDPOINT-5-R02

Round Name: Final EXTERNAL-ENDPOINT Verification Prep

本轮目标:

完成 EXTERNAL-ENDPOINT 批次最终验证准备，跑全量验证，写最终 worker summary，并停止等待 Piko-verify。

本轮任务:
- 执行任务:
  - 汇总 EXTERNAL-ENDPOINT-1 到 EXTERNAL-ENDPOINT-5 所有 artifacts 和 summaries。
  - 更新 docs/current_state 或相关文档，说明 external approved endpoint pilot 的 success/blocked 状态。
  - 更新 `.piko/round_status.json` 为 ready_for_verify 或 blocked_for_external_endpoint。
- 测试任务:
  - 运行 `python -m pytest tests\test_discovery_search.py -q`
  - 运行 `python -m pytest`
  - 运行 EXTERNAL-ENDPOINT 专项测试。
  - 运行 artifact JSON parse probes。
  - 运行 guardrail scan。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-5-R02.md`
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-5.md`
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5.md`

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/external_endpoint/*`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-5-R02.md`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-5.md`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-1-to-EXTERNAL-ENDPOINT-5.md`
- `.piko/round_status.json`

禁止修改:

- 不进入下一批次。
- 不发布、不部署。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- EXTERNAL-ENDPOINT 专项测试
- Artifact JSON parse probes
- Guardrail scan

完成定义:

- EXTERNAL-ENDPOINT 全批次可交给 Piko-verify。
- 外部 endpoint 成功或安全 blocked 状态都清楚记录。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
