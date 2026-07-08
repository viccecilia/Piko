# Round ID: DOMAIN-2-R02

Round Name: Gaming Adapter Compatibility Layer

本轮目标:

建立兼容层，让旧的游戏发现/排行/文章包能力通过 gaming domain pack 继续工作。

本轮任务:
- 执行任务:
  - 实现或定义 compatibility adapter。
  - 将 existing discovery output 映射到 generic contracts。
  - 输出 compatibility artifact。
- 测试任务:
  - 跑现有 `tests\test_discovery_search.py -q`。
  - 测试 gaming adapter output 可被 cross-domain router 接收。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-2-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/domain_plugins/*`
- `.piko/summaries/worker_DOMAIN-2-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不让 gaming 兼容层吞掉错误。

必须运行的验证:

- Gaming compatibility tests
- `python -m pytest tests\test_discovery_search.py -q`

完成定义:

- 旧游戏能力不回归，同时进入 domain pack 架构。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
