# Round ID: ENDPOINT-2-R01

Round Name: Local Endpoint HTTP Surface

本轮目标:

实现或暴露本地 approved endpoint HTTP surface，使测试/worker 能通过 URL 访问 JSON payload。

本轮任务:
- 执行任务:
  - 新增本地 endpoint route 或 lightweight server entry。
  - 返回 approved endpoint fixture JSON。
  - 添加 no-cache / internal-only metadata。
- 测试任务:
  - API probe 返回 200 JSON。
  - Contract validation 通过。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_ENDPOINT-2-R01.md`。

允许修改:

- `apps/*`
- `packages/*`
- `tests/*`
- `artifacts/local_endpoint/*`
- `.piko/summaries/worker_ENDPOINT-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不暴露 secrets。
- 不读取外部网络。

必须运行的验证:

- Local endpoint route tests

完成定义:

- 本地 URL 可返回 approved JSON payload。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
