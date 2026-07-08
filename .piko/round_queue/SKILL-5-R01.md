# Round ID: SKILL-5-R01

Round Name: Social Platform Adapter Contract

本轮目标:

建立社交平台分发 adapter contract，为未来一键发送到小红书、公众号、抖音等平台做准备。

本轮任务:
- 执行任务:
  - 定义 platform adapter contract。
  - 平台至少包含 xiaohongshu、wechat_official_account、douyin，允许扩展 bilibili/twitter/reddit。
  - 字段包含 platform_id、content_fields、media_fields、credential_policy、approval_required、rate_limit_policy、dry_run_supported。
- 测试任务:
  - 测试每个平台默认 dry_run_supported=true。
  - 测试 approval_required=true。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-5-R01.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/social_distribution/*`
- `.piko/summaries/worker_SKILL-5-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不连接真实平台账号。
- 不保存 credentials。

必须运行的验证:

- Platform adapter contract tests

完成定义:

- Piko 有一键分发的 adapter 标准，但默认只 dry-run。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
