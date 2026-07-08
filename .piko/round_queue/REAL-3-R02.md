# Round ID: REAL-3-R02

Round Name: Live Player Pain Buckets

本轮目标:

基于真实 player question signals 生成高热痛点 buckets：已有答案、未解决监控、冲突答案、高风险阻断、必须查攻略。

本轮任务:
- 执行任务:
  - 生成 pain buckets artifact。
  - 每个 bucket 保留代表问题、source ids、answer_status、risk_level、actionability、why_it_matters。
  - watchlist/high-risk 不得进入 normal publish candidate。
- 测试任务:
  - 测试 bucket 分类。
  - 测试 high-risk blocked。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REAL-3-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_REAL-3-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不把无答案高热问题写成已解决。

必须运行的验证:

- Pain bucket tests

完成定义:

- 玩家痛点按漏斗清楚分层。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
