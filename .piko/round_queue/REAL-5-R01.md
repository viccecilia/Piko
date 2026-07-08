# Round ID: REAL-5-R01

Round Name: Operator Real Data Result Surface

本轮目标:

让 operator 能看到真实数据结果：Top 5、痛点 buckets、候选文章包、真实采集状态、阻断原因。

本轮任务:
- 执行任务:
  - 新增或扩展 API/window/operator result。
  - 展示 real_collection_performed、Top 5、pain buckets、selected topic、article package status、publish readiness。
  - 如果 blocked_for_endpoint，页面要明确说明缺什么配置。
- 测试任务:
  - API/window probe 如果实现。
  - HTML 无外部 URL/CDN。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REAL-5-R01.md`。

允许修改:

- `apps/*`
- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_REAL-5-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不让窗口执行发布/部署/采集。
- 不引用外部 CDN。

必须运行的验证:

- Operator result surface tests

完成定义:

- 人能在窗口/API 里看懂真实数据跑到哪一步。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
