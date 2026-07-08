# Round ID: REALDATA-6-R01
Round Name: Realdata Operator Surface

本轮目标:

提供 operator API/window，让人能看到每个真实 provider 的采集、过滤、合并、选题、内容包状态。

本轮任务:
- 执行任务:
  - 新增 `/realdata/result` 和 `/realdata/window` 或等价路由。
  - 页面展示：provider 状态、真实采集、覆盖范围、热门游戏、问题桶、selected topic、内容包、发布 gate。
  - 输出 `artifacts/realdata/latest_realdata_operator_result.json`。
- 测试任务:
  - API probe 200。
  - Window HTML 不引用外部 URL/CDN。
  - 页面中文栏目完整。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-6-R01.md`。

允许修改:

- `apps/api/routes/**`
- `apps/api/main.py`
- `packages/realdata/**`
- `tests/**`
- `artifacts/realdata/**`

禁止修改:

- 打开窗口不得触发真实采集。
- 页面不得暴露 endpoint URL 全量或 secrets。

必须运行的验证:

- REALDATA API/window 专项测试
- HTML external URL guardrail scan

完成定义:

- operator 能直观看到真实数据链路状态和限制。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

