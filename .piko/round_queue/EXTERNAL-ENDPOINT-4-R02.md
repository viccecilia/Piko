# Round ID: EXTERNAL-ENDPOINT-4-R02

Round Name: External Candidate Article Package

本轮目标:

成功时基于 external REAL handoff 生成 internal candidate article package；blocked 时不生成假文章。

本轮任务:
- 执行任务:
  - 生成 article candidate artifact。
  - 包含 source/evidence trace、outline、verification_required=true、publish_ready=false、publishing_performed=false。
  - blocked/failed 时输出 no_candidate_reason。
- 测试任务:
  - 测试 source/evidence trace。
  - 测试 publish disabled。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_EXTERNAL-ENDPOINT-4-R02.md` 和 `.piko/summaries/worker_EXTERNAL-ENDPOINT-4.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/external_endpoint/*`
- `artifacts/article_drafts/*`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-4-R02.md`
- `.piko/summaries/worker_EXTERNAL-ENDPOINT-4.md`
- `.piko/round_status.json`

禁止修改:

- 不发布、不上传。

必须运行的验证:

- External article candidate tests

完成定义:

- 外部 endpoint 成功路径能产出内部候选文章包，或正确 blocked。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
