# Round ID: FINISH-4-R02
Round Name: Human Approval Contract

本轮目标:

明确人类最后确认边界：哪些动作可以自动，哪些动作必须人工确认，哪些动作永远禁止自动。

本轮任务:
- 执行任务:
  - 建立 final MVP human approval contract artifact。
  - 标记 publish、upload、credential use、external connector activation、active plugin replacement 都需要 approval。
  - 将 approval state 接入 operator console。
- 测试任务:
  - 测试缺 approval 时 publish/distribution blocked。
  - 测试 approval artifact 不含真实凭据。
  - 测试 verification gate 不可被 approval bypass。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_FINISH-4-R02.md` 和 `.piko/summaries/worker_FINISH-4.md`。

允许修改:

- `packages/final_mvp/**`
- `packages/skills/**`
- `tests/**`
- `artifacts/final_mvp/**`
- `docs/**`

禁止修改:

- 不得新增 admin 后台真实审批系统。
- 不得把 approval 默认为 true。
- 不得发布或上传。

必须运行的验证:

- human approval contract 专项测试
- full pytest

完成定义:

- 人类确认边界被机器可读和文档化。
- 默认 blocked_for_human_approval。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

