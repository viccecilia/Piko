# Round ID: GROW-1-R01

Round Name: Daily GitHub Scan Intake Contract

本轮目标:

建立每日 GitHub/OSS 扫描结果的 intake contract，让 GROW 队列能稳定读取 `piko-github` 的日报、memory 和本地 OSS artifacts。

本轮任务:
- 执行任务:
  - 定义 daily scan intake schema，至少包含 `scan_date`、`source_thread_id`、`source_memory_path`、`projects`、`candidate_recommendations`、`used_latest_or_fallback`。
  - 支持读取来源：
    - `C:\Users\pangv\.codex\automations\piko-github\memory.md`
    - `artifacts/oss_research/*`
    - 可选的每日 scan report artifact。
  - 若当天扫描不存在，必须使用最近一次结果并明确标记 `used_latest_or_fallback=true`。
  - 生成 `artifacts/growth_loop/latest_scan_intake.json`。
- 测试任务:
  - 测试 intake JSON 可解析。
  - 测试无当天扫描时不会伪装为当天 live scan。
  - 测试每个 project 至少有 name/source/relevance/risk。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_GROW-1-R01.md`。

允许修改:

- `packages/*`
- `apps/api/routes/*`
- `tests/*`
- `docs/*`
- `artifacts/growth_loop/*`
- `.piko/summaries/worker_GROW-1-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要修改 `piko-github` automation 配置。
- 不要联网重新扫描 GitHub，除非后续 round 明确允许。
- 不要自动创建执行任务。

必须运行的验证:

- Scan intake JSON parse probe。
- 相关新增 tests。

完成定义:

- GROW 能读取每日扫描结果，并明确当天/最近一次来源状态。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
