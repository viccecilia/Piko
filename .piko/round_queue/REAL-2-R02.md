# Round ID: REAL-2-R02

Round Name: Real Collection Metadata And Source Coverage

本轮目标:

记录真实采集覆盖范围，说明当前数据来自哪些平台/地区/类型，以及哪些仍然缺失。

本轮任务:
- 执行任务:
  - 生成 source coverage artifact。
  - 字段包含 source_types、source_regions、counts、missing_sources、coverage_level、real_collection_performed。
  - 区分真实覆盖与计划覆盖。
- 测试任务:
  - 测试 coverage 不夸大全网覆盖。
  - 测试 missing_sources 保留。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REAL-2-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/real_data_pilot/*`
- `.piko/summaries/worker_REAL-2-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不声称覆盖 Steam/Reddit/JP/KR，除非 endpoint 数据确实包含。

必须运行的验证:

- Source coverage tests

完成定义:

- Operator 能看清真实覆盖范围和缺口。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
