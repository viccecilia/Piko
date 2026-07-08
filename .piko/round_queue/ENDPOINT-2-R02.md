# Round ID: ENDPOINT-2-R02

Round Name: Explicit Local Opt-In Runner

本轮目标:

建立只在测试/CLI 中使用的显式 local opt-in runner，不改变默认环境。

本轮任务:
- 执行任务:
  - 定义 local opt-in command/helper。
  - 设置 `PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true`、`PIKO_LIVE_DISCOVERY_TEST=true`、local endpoint URL，仅限子进程/测试上下文。
  - 生成 opt-in artifact。
- 测试任务:
  - 测试默认环境仍不触网。
  - 测试 opt-in 只在 runner 范围内生效。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_ENDPOINT-2-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/local_endpoint/*`
- `.piko/summaries/worker_ENDPOINT-2-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不把 opt-in 写成全局默认。

必须运行的验证:

- Local opt-in tests

完成定义:

- 可显式跑 live success path，但默认仍安全关闭。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
