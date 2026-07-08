# Round ID: CONNECTOR-5-R01

Round Name: Operator Connector Surface

本轮目标:

让 operator 能看到 connector registry、domain packs、blocked reasons、dry-run plan、readiness score。

本轮任务:
- 执行任务:
  - 新增或扩展 connector API/window。
  - 展示 connectors、domains、status、approval_required、missing_env、blocked_reason、readiness_score。
  - Surface 必须只读，不执行采集。
- 测试任务:
  - API/window probe 如果实现。
  - HTML 无外部 URL/CDN。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CONNECTOR-5-R01.md`。

允许修改:

- `apps/*`
- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/connector_registry/*`
- `.piko/summaries/worker_CONNECTOR-5-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不让窗口按钮触发真实采集。

必须运行的验证:

- Operator connector surface tests

完成定义:

- Operator 能清楚看到 connector 状态和下一步缺口。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
