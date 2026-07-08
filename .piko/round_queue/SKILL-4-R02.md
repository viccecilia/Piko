# Round ID: SKILL-4-R02

Round Name: Rewrite And Structure Engine

本轮目标:

建立文案重写与结构引擎，把 raw brief 转成更适合传播的标题、引言、正文结构、总结。

本轮任务:
- 执行任务:
  - 生成 rewrite package artifact。
  - 产出标题候选、开头钩子、三段式讲解结构、结论、CTA。
  - 支持“技术项目介绍”和“游戏攻略内容”两类模板。
- 测试任务:
  - 测试输出包含 source/evidence trace。
  - 测试不夸大、不伪造事实。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-4-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/content_quality/*`
- `.piko/summaries/worker_SKILL-4-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不生成虚假亲测/虚假数据。

必须运行的验证:

- Rewrite package tests

完成定义:

- Piko 能把候选素材整理成更强的可发布文案包。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
