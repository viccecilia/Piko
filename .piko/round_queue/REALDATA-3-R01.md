# Round ID: REALDATA-3-R01
Round Name: Freshness Provenance Model

本轮目标:

给真实数据增加 freshness/provenance 模型，确保 Piko 知道数据来自哪里、什么时候观察到、是否过期。

本轮任务:
- 执行任务:
  - 增加 `fetched_at`、`observed_at`、`provider_id`、`source_category`、`source_url`、`freshness_status`。
  - 输出 `artifacts/realdata/latest_provider_freshness.json`。
  - stale 数据不得进入最高优先级 publish candidate。
- 测试任务:
  - 测试 recent / stale / unknown freshness。
  - 测试 stale 降权。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-3-R01.md`。

允许修改:

- `packages/realdata/**`
- `packages/discovery/**`
- `tests/**`
- `artifacts/realdata/**`

禁止修改:

- 不得覆盖真实 fetched_at。
- 不得丢失 source_url/source_category。

必须运行的验证:

- REALDATA freshness 专项测试

完成定义:

- freshness/provenance 可供 verify 和 operator 检查。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

