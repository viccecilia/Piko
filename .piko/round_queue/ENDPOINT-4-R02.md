# Round ID: ENDPOINT-4-R02

Round Name: Internal Article Handoff From Local Live Data

本轮目标:

基于 local live REAL handoff 生成 internal article handoff/readiness，不发布。

本轮任务:
- 执行任务:
  - 生成 internal article handoff artifact。
  - 包含 selected topic、source ids、evidence trace、outline、verification_required=true。
  - 设置 publish_ready=false、publishing_performed=false。
- 测试任务:
  - 测试 source/evidence trace 完整。
  - 测试不发布。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_ENDPOINT-4-R02.md` 和 `.piko/summaries/worker_ENDPOINT-4.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/article_drafts/*`
- `artifacts/publish_readiness/*`
- `artifacts/local_endpoint/*`
- `.piko/summaries/worker_ENDPOINT-4-R02.md`
- `.piko/summaries/worker_ENDPOINT-4.md`
- `.piko/round_status.json`

禁止修改:

- 不发布、不上传。

必须运行的验证:

- Internal article handoff tests

完成定义:

- 本地 live 数据可产出内部候选内容包。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
