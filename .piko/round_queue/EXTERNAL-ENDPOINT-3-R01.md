# Round ID: EXTERNAL-ENDPOINT-3-R01

Round Name: Normalize External Signals

本轮目标:

成功时将外部 endpoint payload normalize 为 generic/domain signals；blocked/failed 时不生成假信号。

本轮任务:
- 执行任务:
  - 生成 external normalized signals artifact。
  - 包含 source ids、source types、domains、need clusters、bounded snippets。
  - scope=external_approved_endpoint。
- 测试任务:
  - 测试成功/blocked 分支。
  - 测试 prohibited fields 不出现。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-3-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/external_endpoint/*`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不用 local fixture 冒充 external。

必须运行的验证:

- External normalization tests

完成定义:

- 外部 approved endpoint 数据进入通用信号层，或正确 blocked。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
