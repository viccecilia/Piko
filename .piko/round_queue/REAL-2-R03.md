# Round ID: REAL-2-R03

Round Name: Real Data Safety Summary

本轮目标:

生成真实数据安全摘要，确认没有保存长原文、隐私/凭据、未批准内容。

本轮任务:
- 执行任务:
  - 生成 safety summary artifact。
  - 字段包含 raw_body_saved=false、full_posts_saved=false、secrets_retained=false、crawler_used=false、publishing_performed=false。
  - 对 artifacts 做 bounded scan。
- 测试任务:
  - 测试安全字段均为 false。
  - 测试敏感字段名不出现在数据 payload 中。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REAL-2-R03.md` 和 `.piko/summaries/worker_REAL-2.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_REAL-2-R03.md`
- `.piko/summaries/worker_REAL-2.md`
- `.piko/round_status.json`

禁止修改:

- 不删除失败证据来逃避扫描。

必须运行的验证:

- Safety summary tests
- Guardrail scan

完成定义:

- 真实数据采集安全边界可验证。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
