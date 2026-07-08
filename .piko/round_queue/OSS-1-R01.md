# Round ID: OSS-1-R01

Round Name: GitHub Research Intake Contract

本轮目标:

定义每日 GitHub 开源项目扫描结果的结构化输入合同，让 Piko 可以稳定读取、比较和复用外部项目研究结果。

本轮任务:
- 执行任务:
  - 定义 OSS research intake schema，至少包含 project_name、github_url、stars、license、domain、category、observed_patterns、piko_relevance、risks、source_date。
  - 支持 categories：agent framework、workflow orchestration、RAG/evidence indexing、plugin architecture、connector framework、evaluation/guardrail、automation、operator UI、content pipeline、self-improvement、video/content skill。
  - 输出或更新 `artifacts/oss_research/daily/*` 的样例 artifact。
  - 明确本轮只建立研究读取合同，不默认联网，不自动改代码。
- 测试任务:
  - 增加或更新 schema/loader 测试，验证合法日报可解析。
  - 测试缺少必填字段时会失败。
  - 测试 license/risk 字段存在。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-1-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/oss_research/*`
- `.piko/summaries/worker_OSS-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要把 GitHub API 调用设为默认测试路径。
- 不要 vendor 外部 repo。
- 不要复制外部项目源码。
- 不要发布、部署、commit、push。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- 新增 OSS schema 测试。

完成定义:

- OSS research intake schema 和 loader 可用。
- 每日扫描结果可被 Piko 结构化读取。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
