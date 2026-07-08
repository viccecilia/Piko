# Round ID: ENDPOINT-1-R02

Round Name: Local Endpoint Fixture Safety

本轮目标:

确保本地 endpoint fixture 没有 raw/full source、secrets、未授权内容或不合规字段。

本轮任务:
- 执行任务:
  - 生成 fixture safety artifact。
  - 检查 prohibited fields。
  - 明确 snippet bounds 和 source trace。
- 测试任务:
  - 测试 fixture 不含 raw_text/body/full_comments。
  - 测试 credentials/secrets 不存在。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_ENDPOINT-1-R02.md` 和 `.piko/summaries/worker_ENDPOINT-1.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/local_endpoint/*`
- `.piko/summaries/worker_ENDPOINT-1-R02.md`
- `.piko/summaries/worker_ENDPOINT-1.md`
- `.piko/round_status.json`

禁止修改:

- 不放宽 endpoint contract。

必须运行的验证:

- Fixture safety tests

完成定义:

- 本地 endpoint fixture 可安全用于 live success path。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
