# Round ID: STORY-4-R02

Round Name: Template Evolution And Final Summary

本轮目标:

允许系统吸收用户以后提供的优秀文章结构，但只能作为 candidate template，不自动替换 active template。

本轮任务:
- 执行任务:
  - 如果 `artifacts/storytelling/template_candidates/*` 存在，读取并生成候选模板摘要。
  - 更新 `artifacts/storytelling/template_registry.json`，把新结构记录为 `candidate`。
  - 不改变 active template，除非本轮任务文件明确要求并验证通过。
  - 生成 STORY batch 总结。
- 测试任务:
  - 验证 active template 仍是 `agent-skill-storytelling:v1`。
  - 验证 candidate template 不影响今日内容生成。
  - 验证 registry JSON 可解析。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_STORY-4-R02.md`。
  - 生成 `.piko/summaries/worker_STORY-4.md`。
  - 生成 `.piko/summaries/worker_storytelling_content_batch.md`。

允许修改:

- `artifacts/storytelling/*`
- `.piko/summaries/worker_STORY-4-R02.md`
- `.piko/summaries/worker_STORY-4.md`
- `.piko/summaries/worker_storytelling_content_batch.md`
- `.piko/round_status.json`

禁止修改:

- 不要自动替换 active template。
- 不要发布、上传、部署、commit 或 push。

必须运行的验证:

- Registry active template probe。
- Final artifact existence probe。

完成定义:

- STORY-0 到 STORY-4 全部完成。
- 生成今日内容包和视频草稿。
- 状态停止，等待 Piko-verify 总体验收。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
