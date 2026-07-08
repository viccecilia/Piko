# Round ID: SOURCE-PROVIDER-2-R01

Round Name: Approved JSON Payload Package

本轮目标:

生成可托管到外部 URL 的 approved JSON payload 文件，符合 Piko approved endpoint contract。

本轮任务:
- 执行任务:
  - 生成 source provider payload artifact/file。
  - 内容可基于现有 approved endpoint fixture，但要标记 provider_package_scope=deploy_ready_static_json。
  - 不包含 raw/full source 或 secrets。
- 测试任务:
  - 运行 approved endpoint contract validation。
  - 测试 prohibited fields 不存在。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SOURCE-PROVIDER-2-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/source_provider/*`
- `.piko/summaries/worker_SOURCE-PROVIDER-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不声称已经外部托管。

必须运行的验证:

- Approved payload contract tests

完成定义:

- 有一个可上传托管的 approved JSON payload。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
