# Round ID: OSS-2-R01

Round Name: Architecture Pattern Extraction

本轮目标:

从候选开源项目中提炼可借鉴的架构模式，而不是复制源码。

本轮任务:
- 执行任务:
  - 读取 `latest_ranked_projects.json`。
  - 为每个候选提取 reusable_patterns，例如 agent runtime boundary、tool registry、skill routing、state machine、evaluation harness、connector adapter、memory strategy、operator UI。
  - 保存 `artifacts/oss_research/latest_patterns.json`。
  - 每个 pattern 必须包含 source_project、summary、why_it_matters、piko_mapping_hint、risk。
- 测试任务:
  - 验证 pattern artifact JSON 可解析。
  - 验证每个 pattern 都有 source_project 和 risk。
  - 验证没有保存外部项目源码片段。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_OSS-2-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/oss_research/*`
- `.piko/summaries/worker_OSS-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要复制外部代码。
- 不要 vendor repo。
- 不要绕过 license 风险。

必须运行的验证:

- Pattern artifact JSON parse probe。
- Guardrail scan for copied source/vendor directories。

完成定义:

- 外部项目被转化为架构模式和设计启发，而不是源码复制。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
