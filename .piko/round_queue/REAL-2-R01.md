# Round ID: REAL-2-R01

Round Name: Real Payload Normalization

本轮目标:

将通过合同验证的 live payload normalize 为 GameHeatSignal 和 PlayerQuestionSignal。若 REAL-1 blocked，则本轮不应伪造真实数据。

本轮任务:
- 执行任务:
  - 从 live verification result 读取 bounded normalized data。
  - 生成 normalized real signals artifact。
  - 保留 source summary、source type、region、snippet bounded fields。
- 测试任务:
  - 测试 prohibited fields 不进入 artifact。
  - 测试 real_collection_performed 与 verification evidence 一致。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REAL-2-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_REAL-2-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不保存 raw_text/body/selftext/full_comments/raw_page_text。
- 不进行 crawler。

必须运行的验证:

- Normalization tests
- Prohibited field scan

完成定义:

- 真实数据被规范化为安全信号。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
