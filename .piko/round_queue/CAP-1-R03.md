# Round ID: CAP-1-R03

Round Name: Capability Scorecard Artifact

本轮目标:

把当前能力图套用评分政策，生成第一版 capability scorecard。

本轮任务:
- 执行任务:
  - 读取 latest capability map 和 evaluation policy。
  - 生成 `artifacts/capability_map/latest_capability_scorecard.json`。
  - Scorecard 包含每个 capability 的 score、decision、evidence、recommended_action、requires_human_approval。
  - 输出 top improvement targets 和 top replacement candidates。
- 测试任务:
  - scorecard JSON 可解析。
  - 每个 replacement candidate 都有 reason 和 rollback expectation。
  - 不直接触发替换。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-1-R03.md`。
  - 生成 `.piko/summaries/worker_CAP-1.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_CAP-1-R03.md`
- `.piko/summaries/worker_CAP-1.md`
- `.piko/round_status.json`

禁止修改:

- 不要替换或删除能力。
- 不要自动执行 recommended_action。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- scorecard JSON parse probe

完成定义:

- CAP-1 三个 round summary 和 stage summary 存在。
- 第一版 capability scorecard 可用于后续优化。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
