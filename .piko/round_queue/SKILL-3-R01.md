# Round ID: SKILL-3-R01

Round Name: Declarative Eval Spec

本轮目标:

建立 promptfoo-style declarative eval spec，用于高风险 skill/agent 的回归测试。

本轮任务:
- 执行任务:
  - 定义 eval spec schema：case_id、input、expected_signals、forbidden_outputs、risk_tags、pass_criteria。
  - 支持 JSON 或 YAML-like JSON。
  - 创建 content quality 和 social distribution 的示例 eval suite。
- 测试任务:
  - 测试 eval spec 可解析。
  - 测试 forbidden_outputs 命中时 fail。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-3-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/declarative_eval/*`
- `.piko/summaries/worker_SKILL-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不让 declarative eval 替代 Piko-verify。

必须运行的验证:

- Eval spec tests

完成定义:

- Piko 有可重复运行的 declarative eval 入口。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
