# Round ID: LIVE-CONNECTOR-3-R01

Round Name: Normalize Live Connector Signals

本轮目标:

成功 live collection 时，将数据 normalize 为 generic source signals / need clusters；blocked 时保持空结果并说明原因。

本轮任务:
- 执行任务:
  - 生成 normalized live signals artifact。
  - 支持 generic contract 和 domain-specific payload。
  - 保留 source ids、source types、regions、bounded snippets。
- 测试任务:
  - 测试 prohibited fields 不出现。
  - 测试 blocked 时不生成假 signals。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_LIVE-CONNECTOR-3-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/live_connector_pilot/*`
- `.piko/summaries/worker_LIVE-CONNECTOR-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不伪造 live signals。

必须运行的验证:

- Live normalization tests

完成定义:

- live 数据进入通用信号层，或正确 blocked。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
