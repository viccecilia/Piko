# Round ID: FINISH-1-R01
Round Name: External Endpoint Configuration Gate

本轮目标:

确认 Piko 是否具备真实外部 approved JSON endpoint 运行条件，并把缺失项以机器可读 artifact 和 operator 可读说明输出。

本轮任务:
- 执行任务:
  - 读取 SOURCE-PROVIDER handoff 和 EXTERNAL-ENDPOINT env 约定。
  - 检查 `PIKO_ENABLE_DISCOVERY_REAL_SOURCE`、`PIKO_LIVE_DISCOVERY_TEST`、`PIKO_APPROVED_ENDPOINT_URL`。
  - 拒绝 localhost、127.0.0.1、file、fixture、mock、相对路径。
  - 输出 `artifacts/final_mvp/latest_external_live_result.json` 的初始状态。
- 测试任务:
  - 增加或更新 FINISH endpoint gate 测试，覆盖缺 env、local URL、fixture URL、合法 HTTPS URL 形态。
  - 运行 FINISH 专项测试。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_FINISH-1-R01.md`。

允许修改:

- `packages/final_mvp/**`
- `packages/external_endpoint/**`
- `packages/source_provider/**`
- `tests/**`
- `artifacts/final_mvp/**`
- `docs/**`
- `.piko/summaries/**`

禁止修改:

- 不得删除既有测试。
- 不得把 fixture/local/mock 标成 external success。
- 不得保存 credentials、token、cookie、authorization。
- 不得发布、部署、上传。

必须运行的验证:

- FINISH endpoint gate 专项测试
- `python -m pytest tests\test_external_endpoint_pilot.py -q`

完成定义:

- endpoint 配置状态清楚。
- 缺配置时明确 blocked。
- 合法配置时可进入 FINISH-1-R02。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

