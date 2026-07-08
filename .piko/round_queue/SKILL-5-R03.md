# Round ID: SKILL-5-R03

Round Name: One-Click Distribution Dry Run

本轮目标:

实现一键分发 dry-run：把多平台内容包打包成待发送队列，显示每个平台准备状态，但不真实发送。

本轮任务:
- 执行任务:
  - 生成 distribution dry-run package。
  - 字段包含 package_id、platform_targets、content_refs、media_refs、preflight_status、approval_status、dispatch_performed=false。
  - 生成 operator-facing summary。
- 测试任务:
  - 测试 dispatch_performed=false。
  - 测试缺 approval 或 credential 时 blocked_for_approval/blocked_for_credentials。
  - 运行全量验证并生成最终 summary。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_SKILL-5-R03.md`
  - 生成 `.piko/summaries/worker_SKILL-5.md`
  - 生成 `.piko/summaries/worker_SKILL-1-to-SKILL-5.md`

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/social_distribution/*`
- `artifacts/content_quality/*`
- `.piko/summaries/worker_SKILL-5-R03.md`
- `.piko/summaries/worker_SKILL-5.md`
- `.piko/summaries/worker_SKILL-1-to-SKILL-5.md`
- `.piko/round_status.json`

禁止修改:

- 不真实发布、不上传、不调用平台发布 API。
- 不进入下一批次。

必须运行的验证:

- `python -m pytest tests\test_discovery_search.py -q`
- `python -m pytest`
- SKILL 专项测试
- Artifact JSON parse probes
- Guardrail scan

完成定义:

- Piko 能生成一键分发 dry-run 队列。
- 真实分发仍需人工批准和凭据安全通道。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
