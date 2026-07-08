# Round ID: CAP-3-R01

Round Name: Autonomous Workflow Levels

本轮目标:

定义 Piko 自动化等级，让系统逐步接近“人类只做最后确认”，但不会越权。

本轮任务:
- 执行任务:
  - 定义 automation levels：
    - L0 manual only
    - L1 assisted proposal
    - L2 worker executes with tests
    - L3 worker executes and verify gates approve
    - L4 autonomous scheduled run with human final approval
    - L5 full autonomous publish/deploy，当前禁止
  - 为每类任务定义最高允许等级。
  - 输出 `artifacts/capability_map/autonomy_policy.json`。
- 测试任务:
  - policy JSON 可解析。
  - publish/deploy/credential use/license-risk adoption 必须 human approval。
  - L5 标记 disabled。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-3-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_CAP-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要开启 full autonomous publish/deploy。
- 不要默认使用 credentials。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- autonomy policy JSON parse probe

完成定义:

- Piko 自动化等级和边界明确。
- 人类最后确认角色被保留。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
