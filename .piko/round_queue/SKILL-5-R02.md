# Round ID: SKILL-5-R02

Round Name: Approval And Credential Safety Gate

本轮目标:

建立社交分发前的 approval 和 credential safety gate，避免误发、泄露账号或平台违规。

本轮任务:
- 执行任务:
  - 定义 distribution approval artifact。
  - 定义 credential policy：不保存 token/cookie/API key；只允许外部安全输入或平台官方授权。
  - 定义 preflight checklist：内容、版权、平台字段、敏感词、频率限制、人工确认。
- 测试任务:
  - 测试无 approval 不可 dispatch。
  - 测试任何 credential-like 字段被拒绝或 redacted。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-5-R02.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/social_distribution/*`
- `.piko/summaries/worker_SKILL-5-R02.md`
- `.piko/round_status.json`

禁止修改:

- 不存储真实账号凭据。
- 不绕过平台审核。

必须运行的验证:

- Approval/credential guardrail tests

完成定义:

- 一键分发有强制人工确认和凭据安全边界。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
