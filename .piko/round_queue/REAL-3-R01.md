# Round ID: REAL-3-R01

Round Name: Live Hot Game Rankings

本轮目标:

基于真实 normalized signals 生成当前热门游戏 Top 5 / Top 20。若无真实数据，必须标记 blocked/empty，不回退伪装 fixture。

本轮任务:
- 执行任务:
  - 运行 live ranking。
  - 输出 Top 5 / Top 20 artifact。
  - 每个游戏包含 heat score、source evidence、region/source diversity、reason summary。
- 测试任务:
  - 测试 Top 5 来自 real normalized signals 或明确 blocked。
  - 测试 real_collection_performed 状态一致。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REAL-3-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_REAL-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不用 fixture 冒充 live ranking。

必须运行的验证:

- Live ranking tests

完成定义:

- 当前热门游戏排行真实可信，或明确 blocked。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
