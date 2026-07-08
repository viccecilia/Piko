# Round ID: REALDATA-3-R02
Round Name: Cross-Provider Dedup And Cluster Merge

本轮目标:

跨 provider 去重并合并同类玩家问题，保留代表问题和所有来源 trace。

本轮任务:
- 执行任务:
  - 对相同 game + need intent + question text 近似项聚类。
  - 保留 representative_question_id、source_count、source_categories、regions、deduped_question_ids。
  - 不合并高风险 save recovery 与普通 save location。
- 测试任务:
  - 测试 Steam/Reddit 同问题合并。
  - 测试 JP/KR minority-language example 保留。
  - 测试 high-risk 不误并。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-3-R02.md` 和 `.piko/summaries/worker_REALDATA-3.md`。

允许修改:

- `packages/realdata/**`
- `packages/discovery/**`
- `tests/**`
- `artifacts/realdata/**`

禁止修改:

- 不得丢弃少数语言来源。
- 不得合并不同风险等级的问题。

必须运行的验证:

- REALDATA dedup/cluster 专项测试

完成定义:

- provider 信号被稳定聚类，且 source trace 完整。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

