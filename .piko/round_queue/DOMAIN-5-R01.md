# Round ID: DOMAIN-5-R01

Round Name: Domain-Agnostic Operator Surface

本轮目标:

让 operator surface 展示 Piko 是通用 domain 系统，而不是游戏页面。

本轮任务:
- 执行任务:
  - 新增或扩展 domain operator API/window。
  - 展示 registered domains、domain status、fixture status、workflow route、content package status。
  - 页面文案使用“领域/信号/需求/机会/证据/内容包”，不使用游戏专属词作为主标题。
- 测试任务:
  - API/window probe 如果实现。
  - HTML 无外部 URL/CDN。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-5-R01.md`。

允许修改:

- `apps/*`
- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/domain_plugins/*`
- `.piko/summaries/worker_DOMAIN-5-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不移除 gaming-specific 页面，除非提供兼容入口。

必须运行的验证:

- Operator surface tests

完成定义:

- 人能从界面/API 看出 Piko 是通用可插拔 domain 系统。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
