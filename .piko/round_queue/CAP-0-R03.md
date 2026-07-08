# Round ID: CAP-0-R03

Round Name: Capability Gap Map

本轮目标:

把本地能力和可用外部 skills/connectors 汇总成 Piko 第一版能力图，识别缺口、重复能力和替换候选。

本轮任务:
- 执行任务:
  - 生成 `artifacts/capability_map/latest_capability_map.json`。
  - 输出 capability groups：discovery、evidence、writing、verification、publishing readiness、plugin/domain、connector、automation、operator UI、self-improvement。
  - 标记每个能力：keep、improve、wrap、replace_candidate、defer、reject。
  - 输出当前最大缺口：真实数据 provider、domain plugin runtime、publish approval UI、capability evaluation harness。
- 测试任务:
  - latest capability map JSON 可解析。
  - 至少包含 keep/improve/replace_candidate 三种状态。
  - 不改变 runtime 行为。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-0-R03.md`。
  - 生成 `.piko/summaries/worker_CAP-0.md`。

允许修改:

- `docs/*`
- `artifacts/capability_map/*`
- `tests/*`
- `.piko/summaries/worker_CAP-0-R03.md`
- `.piko/summaries/worker_CAP-0.md`
- `.piko/round_status.json`

禁止修改:

- 不要替换能力。
- 不要删除现有代码。
- 不要默认联网。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- capability map JSON parse probe

完成定义:

- CAP-0 三个 round summary 和 stage summary 存在。
- 第一版能力图可用，并能指导 OSS 学习方向。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
