# Round ID: CONNECTOR-5-R02

Round Name: Final CONNECTOR Verification Prep

本轮目标:

完成 CONNECTOR 批次最终验证准备，跑全量验证，写最终 worker summary，并停止等待 Piko-verify。

本轮任务:
- 执行任务:
  - 汇总 CONNECTOR-1 到 CONNECTOR-5 所有 artifacts 和 summaries。
  - 更新 docs/current_state 或相关文档，说明 connector registry 和 REAL blocked_for_endpoint 的关系。
  - 更新 `.piko/round_status.json` 为 ready_for_verify。
- 测试任务:
  - 运行 `python -m pytest tests\test_discovery_search.py -q`
  - 运行 `python -m pytest`
  - 运行 CONNECTOR 专项测试。
  - 运行 artifact JSON parse probes。
  - 运行 guardrail scan。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-5-R02.md`
  - 生成 `.piko/summaries/worker_CONNECTOR-5.md`
  - 生成 `.piko/summaries/worker_CONNECTOR-1-to-CONNECTOR-5.md`

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-5-R02.md`
- `.piko/summaries/worker_CONNECTOR-5.md`
- `.piko/summaries/worker_CONNECTOR-1-to-CONNECTOR-5.md`
- `.piko/round_status.json`

禁止修改:

- 不进入下一批次。
- 不发布、不部署、不触网采集。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- CONNECTOR 专项测试
- Artifact JSON parse probes
- Guardrail scan

完成定义:

- CONNECTOR 全批次可交给 Piko-verify。
- Piko 有通用 connector registry，但不会默认真实采集。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
