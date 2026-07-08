# Round ID: GROW-3-R03

Round Name: Draft Queue Package

本轮目标:

生成每日 growth draft queue package，供人类决定是否把某个草稿转成正式 round queue。

本轮任务:
- 执行任务:
  - 生成 `artifacts/growth_loop/latest_draft_queue_package.json`。
  - 生成可读 Markdown `artifacts/growth_loop/latest_draft_queue_package.md`。
  - package 必须包含 worker drafts、verify drafts、source CAP decisions、human approval required。
  - 不得写入 `.piko/round_queue` 作为正式可执行 round。
- 测试任务:
  - 验证 JSON 可解析。
  - 验证 package `status=draft_only`。
  - 验证 `.piko/round_queue` 未被自动新增 growth-generated executable round。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_GROW-3-R03.md`。
  - 生成 `.piko/summaries/worker_GROW-3.md`。

允许修改:

- `packages/*`
- `tests/*`
- `docs/*`
- `artifacts/growth_loop/*`
- `.piko/summaries/worker_GROW-3-R03.md`
- `.piko/summaries/worker_GROW-3.md`
- `.piko/round_status.json`

禁止修改:

- 不要自动写正式 round 文件。
- 不要自动发送任务给 worker/verify。

必须运行的验证:

- Draft queue package parse probe。
- No executable round generation probe。

完成定义:

- Piko 能产出每日 worker/verify 草稿包，但仍等待人工确认。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
