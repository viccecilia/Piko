# Round ID: FINISH-4-R01
Round Name: Operator Console Trace Surface

本轮目标:

让 operator 能在一个窗口看到 Piko 的完整动作链：外部来源、筛选漏斗、证据、候选文章、风险、下一步。

本轮任务:
- 执行任务:
  - 新增或扩展 final MVP operator API/window。
  - 展示 external endpoint status、real_collection_performed、top signals、topic funnel、evidence trace、content package、publish gate。
  - 输出 `artifacts/final_mvp/latest_operator_console.json`。
- 测试任务:
  - API probe 返回 200。
  - Window HTML 不引用外部 URL/CDN。
  - 页面包含中文栏目：真实来源状态、热门排行、问题漏斗、证据链、内容包、发布确认。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_FINISH-4-R01.md`。

允许修改:

- `apps/api/routes/**`
- `packages/final_mvp/**`
- `tests/**`
- `artifacts/final_mvp/**`

禁止修改:

- 不得让打开窗口触发真实采集或发布。
- 不得在页面暴露 secrets。
- 不得引外部 CDN。

必须运行的验证:

- API/window probe
- HTML external URL guardrail scan

完成定义:

- operator 能看懂 Piko 每一步做了什么。
- 窗口只读，不产生副作用。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

