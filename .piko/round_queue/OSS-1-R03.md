# Round ID: OSS-1-R03

Round Name: Piko Relevance Scoring

本轮目标:

为开源项目建立 Piko 相关性评分，判断它是应该进入 CAP 能力图候选、STORY 内容候选，还是只记录观察。

本轮任务:
- 执行任务:
  - 定义 relevance score components：piko_goal_fit、maturity、integration_cost、license_safety、testability、replace_existing_skill_value、content_story_value。
  - 输出 recommendation：adopt_candidate、watch、story_only、reject。
  - 输出 handoff_targets：CAP、STORY、both、none。
  - 保存 `artifacts/oss_research/latest_ranked_projects.json`。
- 测试任务:
  - 测试高成熟低风险项目可进入 CAP/STORY。
  - 测试 license 高风险项目不能进入 adopt_candidate。
  - 测试 story_only 项目不会变成 runtime upgrade。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-1-R03.md`。
  - 生成 `.piko/summaries/worker_OSS-1.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/oss_research/*`
- `.piko/summaries/worker_OSS-1-R03.md`
- `.piko/summaries/worker_OSS-1.md`
- `.piko/round_status.json`

禁止修改:

- 不要自动安装依赖。
- 不要自动替换现有 agent/skill。
- 不要发布内容。

必须运行的验证:

- Relevance scoring 测试。
- JSON parse probe for latest ranked projects。

完成定义:

- OSS-1 能输出可排序、可分流的开源项目候选。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
