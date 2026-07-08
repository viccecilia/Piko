# Round ID: REV-3-R01

Round Name: Approved Live Source Registry

本轮目标:

建立真实市场数据源注册表，让 Piko 能明确知道哪些真实 endpoint 是被批准的、属于什么来源类型、允许返回哪些字段、默认是否启用。

本轮任务:
- 执行任务:
  - 新增或扩展 real endpoint/source registry，支持 Steam / Reddit / SERP / JP community / KR community 五类 approved JSON endpoint 配置。
  - 支持从环境变量读取 endpoint URL，但默认禁用真实调用。
  - 每个 source 配置必须包含 source id、source category、region/language、timeout、limit、retained fields、prohibited fields。
  - 明确拒绝 HTML URL、raw body endpoint、不在白名单内的 source category。
  - 文档说明第一版可以使用第三方受控 JSON endpoint，而不是 crawler。
- 测试任务:
  - 增加 registry 单元测试：默认无 endpoint 时安全 disabled/skipped。
  - 增加白名单测试：Steam / Reddit / SERP / JP / KR source category 可注册。
  - 增加拒绝测试：HTML endpoint、未知 source category、raw body 字段配置必须被拒绝或标记 unsupported。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REV-3-R01.md`。
  - Summary 需列出支持的 endpoint env var 名称、默认状态、拒绝规则。

允许修改:

- `packages/discovery/*`
- `packages/collectors/*`
- `tests/test_discovery_search.py`
- `docs/player_pain_discovery.md`
- `docs/current_state.md`
- `.piko/summaries/worker_REV-3-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要真实联网。
- 不要添加 crawler、HTML scraper 或浏览器自动抓站。
- 不要保存 raw response body、完整帖子、完整评论、图片、地图、表格、credentials、secrets。
- 不要发布、部署、commit、push。
- 不要默认调用 LLM 或 translation API。
- 不要绕过 verification 或放宽 Gate。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`

完成定义:

- Approved live source registry 可配置、可测试、默认安全关闭。
- 未配置真实 endpoint 时所有默认测试离线通过。
- 不支持/不安全来源会被拒绝或清晰标记 unsupported。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
