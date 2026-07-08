# Round ID: DOMAIN-1-R01

Round Name: Product Boundary Contract

本轮目标:

明确 Piko 的产品边界：Piko core 是 domain-agnostic pluggable multi-agent system，gaming 只是 domain pack。

本轮任务:
- 执行任务:
  - 生成 product boundary artifact。
  - 明确 core owns：workflow、agent runtime、evidence、trace、eval、quality、distribution dry-run、verify gate。
  - 明确 domain owns：vocabulary、source types、normalizers、scoring presets、templates、risk rules、labels。
- 测试任务:
  - 测试 boundary artifact 可解析。
  - 测试 core_boundary.domain_agnostic=true。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-1-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/domain_plugins/*`
- `.piko/summaries/worker_DOMAIN-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不删除 gaming 能力。
- 不把 gaming 标记为 core。

必须运行的验证:

- Boundary artifact tests

完成定义:

- Piko 的边界不再模糊：core 通用，domain 可插拔。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
