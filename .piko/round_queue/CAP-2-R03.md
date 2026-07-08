# Round ID: CAP-2-R03

Round Name: Capability Registry API And Window Preview

本轮目标:

让 operator 能通过 API/window 查看能力图、scorecard 和 routing policy。

本轮任务:
- 执行任务:
  - 新增或扩展 API endpoint，例如 `/capabilities` 或 `/discovery/capabilities`。
  - 新增或扩展 operator surface，展示：
    - 当前能力列表
    - keep/improve/replace_candidate
    - 需要凭证的能力
    - 需要人类批准的能力
    - fallback route
  - 页面只读，不允许一键替换。
- 测试任务:
  - API probe 返回 capability registry。
  - Window HTML 包含“能力地图”“替换候选”“需要人工确认”等中文文案。
  - 不发生 runtime 替换。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-2-R03.md`。
  - 生成 `.piko/summaries/worker_CAP-2.md`。

允许修改:

- `apps/api/routes/*`
- `apps/web/pages/*`
- `packages/*`
- `tests/*`
- `docs/*`
- `.piko/summaries/worker_CAP-2-R03.md`
- `.piko/summaries/worker_CAP-2.md`
- `.piko/round_status.json`

禁止修改:

- 不要提供自动安装/自动替换按钮。
- 不要发布、部署、commit、push。
- 不要默认联网。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- API/window probe

完成定义:

- CAP-2 三个 round summary 和 stage summary 存在。
- Operator 可查看能力地图和路由策略。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
