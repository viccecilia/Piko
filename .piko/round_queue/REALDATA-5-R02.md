# Round ID: REALDATA-5-R02
Round Name: Realdata Content Package And Readiness

本轮目标:

生成真实数据驱动的内容包和发布前 readiness，不发布。

本轮任务:
- 执行任务:
  - 生成 title options、outline、claim trace、risk notes、platform adaptations。
  - 保留 `publish_ready=false`，`publishing_performed=false`。
  - 输出 distribution readiness but no dispatch。
- 测试任务:
  - 测试 package 包含 source/provider trace。
  - 测试 publish/upload/deploy 全 false。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_REALDATA-5-R02.md` 和 `.piko/summaries/worker_REALDATA-5.md`。

允许修改:

- `packages/realdata/**`
- `packages/skill_runtime/**`
- `tests/**`
- `artifacts/realdata/**`

禁止修改:

- 不得发布、上传、部署。
- 不得保存平台凭据。

必须运行的验证:

- REALDATA content package 专项测试

完成定义:

- 内容包可供人类审核。
- 发布安全字段全部保持 false。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议

