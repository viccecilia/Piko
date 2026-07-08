# Round ID: CAP-4-R01

Round Name: Continuous Capability Update Loop

本轮目标:

把每日 OSS 扫描、能力评分、替换候选和人类确认串成持续优化闭环。

本轮任务:
- 执行任务:
  - 定义 capability update loop：
    - daily OSS research
    - pattern extraction
    - capability candidate scoring
    - replacement policy check
    - task queue candidate generation
    - human approval
    - worker implementation
    - verify validation
    - capability map update
  - 输出 `artifacts/capability_map/capability_update_loop.json`。
  - 文档说明如何增加/减少/替换 skills。
- 测试任务:
  - update loop JSON 可解析。
  - loop 必须包含 human approval 和 verify validation。
  - loop 不允许 auto-install 或 auto-replace。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_CAP-4-R01.md`。

允许修改:

- `docs/*`
- `tests/*`
- `artifacts/capability_map/*`
- `.piko/summaries/worker_CAP-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要修改自动化调度。
- 不要自动安装/替换 skills。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- update loop JSON parse probe

完成定义:

- Piko 有持续能力优化闭环定义。
- 能力增加/减少/替换都必须可验证。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
