# Round ID: GROW-4-R02

Round Name: Growth Operator Window

本轮目标:

提供只读窗口，让这个 Piko 成长窗口能看到每日发现、CAP 判断、草稿任务和阻断原因。

本轮任务:
- 执行任务:
  - 新增或更新 `/growth/window`。
  - 页面至少展示：scan date、candidate count、CAP decisions、draft task count、human approval required、latest risks。
  - 页面必须明确：这是 proposal-only，不自动执行。
- 测试任务:
  - window probe 返回 200。
  - HTML 包含关键文案：Daily Growth、CAP Review、Draft Queue、Human approval required、Proposal only。
  - 页面不引用外部 CDN。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_GROW-4-R02.md`。
  - 生成 `.piko/summaries/worker_GROW-4.md`。

允许修改:

- `apps/api/routes/*`
- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/growth_loop/*`
- `.piko/summaries/worker_GROW-4-R02.md`
- `.piko/summaries/worker_GROW-4.md`
- `.piko/round_status.json`

禁止修改:

- 不要引入外部 CDN。
- 不要加入执行按钮。
- 不要自动发布或部署。

必须运行的验证:

- `/growth/window` probe if implemented。
- HTML external resource scan if HTML generated。

完成定义:

- 操作员有只读 growth dashboard，可看但不能自动执行。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
