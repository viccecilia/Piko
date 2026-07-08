# Round ID: DOMAIN-4-R03

Round Name: Cross-Domain Quality And Distribution Handoff

本轮目标:

证明 content quality 和 distribution dry-run 能接收不同 domain 的 content package。

本轮任务:
- 执行任务:
  - 将 gaming 和 ai_tools content package 都送入 content quality package。
  - 生成 cross-domain distribution dry-run package。
  - 保持 dispatch_performed=false。
- 测试任务:
  - 测试两个 domain 都能生成平台适配内容。
  - 测试 distribution dry-run 不发布。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_DOMAIN-4-R03.md` 和 `.piko/summaries/worker_DOMAIN-4.md`。

允许修改:

- `packages/*`
- `tests/*`
- `artifacts/domain_plugins/*`
- `artifacts/content_quality/*`
- `artifacts/social_distribution/*`
- `.piko/summaries/worker_DOMAIN-4-R03.md`
- `.piko/summaries/worker_DOMAIN-4.md`
- `.piko/round_status.json`

禁止修改:

- 不发布、不上传。

必须运行的验证:

- Cross-domain quality/distribution tests

完成定义:

- 内容质量和分发 dry-run 不再只服务游戏。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
