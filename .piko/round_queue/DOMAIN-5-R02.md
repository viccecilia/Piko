# Round ID: DOMAIN-5-R02

Round Name: Final DOMAIN Verification Prep

本轮目标:

完成 DOMAIN 批次最终验证准备，跑全量验证，写最终 worker summary，并停止等待 Piko-verify。

本轮任务:
- 执行任务:
  - 汇总 DOMAIN-1 到 DOMAIN-5 所有 artifacts 和 summaries。
  - 更新 docs/current_state 或相关文档，说明 Piko 已从 gaming-specific 走向 domain-agnostic plugin system。
  - 更新 `.piko/round_status.json` 为 ready_for_verify。
- 测试任务:
  - 运行 `python -m pytest tests\test_discovery_search.py -q`
  - 运行 `python -m pytest`
  - 运行 DOMAIN 专项测试。
  - 运行 artifact JSON parse probes。
  - 运行 guardrail scan。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-5-R02.md`
  - 生成 `.piko/summaries/worker_DOMAIN-5.md`
  - 生成 `.piko/summaries/worker_DOMAIN-1-to-DOMAIN-5.md`

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/domain_plugins/*`
- `.piko/summaries/worker_DOMAIN-5-R02.md`
- `.piko/summaries/worker_DOMAIN-5.md`
- `.piko/summaries/worker_DOMAIN-1-to-DOMAIN-5.md`
- `.piko/round_status.json`

禁止修改:

- 不进入下一批次。
- 不发布、不部署。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- DOMAIN 专项测试
- Artifact JSON parse probes
- Guardrail scan

完成定义:

- DOMAIN 全批次可交给 Piko-verify。
- Piko 的 domain-agnostic 边界被明确证明。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
