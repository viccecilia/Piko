# Round ID: REALDATA-1-R01
Round Name: Provider Source Contract Expansion

本轮目标:

定义真实 provider 摘要 endpoint 合同，覆盖 Steam、Reddit、SERP、JP community、KR community，并明确 retained/prohibited fields。

本轮任务:
- 执行任务:
  - 复用并扩展 `real_market_source_contract`，生成 `artifacts/realdata/latest_provider_contract.json`。
  - 明确每类 provider 的输入字段、输出字段、最大 snippet 长度、最大记录数、source trace 字段。
  - 标记所有 provider 为 `candidate_only=true`，不是发布许可。
- 测试任务:
  - 覆盖 provider contract schema。
  - 验证 prohibited fields 包含 raw_text/body/selftext/content/full_comments/raw_page_text/credentials/authorization/api_key。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-1-R01.md`。

允许修改:

- `packages/realdata/**`
- `packages/discovery/real_market.py`
- `packages/collectors/**`
- `tests/**`
- `artifacts/realdata/**`
- `.piko/summaries/**`

禁止修改:

- 不得新增 crawler 或 HTML scrape。
- 不得默认启用真实 provider。
- 不得保存 raw/full source。

必须运行的验证:

- REALDATA provider contract 专项测试

完成定义:

- provider 合同机器可读。
- retained/prohibited fields 清楚。
- 五类 provider 都有明确边界。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

