# Round ID: REV-5-R02

Round Name: Solution Source Hints And Evidence Readiness

本轮目标:

对选中的安全 topic 生成解决方案搜索线索和证据准备计划，说明搜索到了哪些解决方案候选，以及哪些还需要进入证据流水线确认。

本轮任务:
- 执行任务:
  - 为 selected candidate 生成 source query hints：游戏名 + 问题类型 + 平台 + 语言/地区 + source type。
  - 从已有 endpoint/mock-live/source hints 中提取 solution candidate signals，但不要把弱信号当最终答案。
  - 输出 evidence readiness preview：已有答案、缺失来源、需要确认的 source types、风险提示。
  - 如果已有文章 artifact 可复用，建立 candidate -> article/evidence handoff 引用。
- 测试任务:
  - source query hints 包含 game、need、representative question、source region、source type。
  - evidence readiness preview 不包含 raw/full source。
  - unanswered/high-risk topic 不产生“已解决”结论。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-5-R02.md`。

允许修改:

- `packages/discovery/*`
- `packages/workflows/*`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`
- `.piko/summaries/worker_REV-5-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不要真实发布。
- 不要抓取或保存完整来源正文。
- 不要用未验证来源生成确定解决方案。
- 不要默认调用 LLM。
- 不要绕过 article verification。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`

完成定义:

- Safe candidate 有清晰 source hints 和 evidence readiness。
- 系统能说明“搜索到了什么解决方案线索”和“还缺什么证据”。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
