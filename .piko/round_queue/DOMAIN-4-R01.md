# Round ID: DOMAIN-4-R01

Round Name: Cross-Domain Router

本轮目标:

建立 cross-domain router，根据 domain_id 选择对应 domain pack、normalizer、scoring profile、content template。

本轮任务:
- 执行任务:
  - 实现或定义 router artifact/API。
  - 支持 gaming 和 ai_tools。
  - unknown domain 返回 safe failed/candidate-only response。
- 测试任务:
  - 测试 gaming route。
  - 测试 ai_tools route。
  - 测试 unknown domain 安全失败。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-4-R01.md`。

允许修改:

- `apps/*`
- `packages/*`
- `tests/*`
- `artifacts/domain_plugins/*`
- `.piko/summaries/worker_DOMAIN-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不让 unknown domain fallback 到 gaming。

必须运行的验证:

- Cross-domain router tests

完成定义:

- Piko 能按 domain 路由，而不是默认游戏。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
