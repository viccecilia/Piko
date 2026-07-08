# Round ID: FINISH-2-R01
Round Name: Real Signal Normalization And Domain Routing

本轮目标:

把通过 external endpoint contract 的真实信号送入通用 domain router，不再走 gaming-only 假设。

本轮任务:
- 执行任务:
  - 将 live games/questions/source summaries normalize 为通用 source_signal / need_cluster 输入。
  - 通过 domain router 判定 gaming、ai_tools 或其他 domain pack。
  - 输出 `artifacts/final_mvp/latest_real_signal_funnel.json` 的 routing section。
- 测试任务:
  - 测试 gaming 与 ai_tools domain routing。
  - 测试 unknown domain safe_fail。
  - 测试 no live success 时本轮不伪造数据。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_FINISH-2-R01.md`。

允许修改:

- `packages/final_mvp/**`
- `packages/domain_plugins/**`
- `packages/discovery/**`
- `tests/**`
- `artifacts/final_mvp/**`

禁止修改:

- 不得把 Piko 改回 gaming-only。
- 不得默认启用 candidate domain。
- 不得跳过 verification gate。

必须运行的验证:

- domain plugin 专项测试
- FINISH funnel 专项测试

完成定义:

- live signal 能进入通用 routing artifact。
- domain-specific 字段只留在 domain pack/display 层。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

