# Piko-worker Task: STORY-0 To STORY-4 Batch

你现在执行 Skill Storytelling And Daily Video Queue。

请从 `C:\PycharmProjects\Piko\.piko\round_queue\STORY-INDEX.md` 开始读取队列，然后按 Stage batch 顺序执行：

```text
STORY-0-R01 -> STORY-0-R02
STORY-1-R01 -> STORY-1-R02
STORY-2-R01 -> STORY-2-R02 -> STORY-2-R03
STORY-3-R01 -> STORY-3-R02 -> STORY-3-R03
STORY-4-R01 -> STORY-4-R02
```

执行规则：

- 每个 round 必须先读取对应 `STORY-*.md` 文件。
- 每完成一个 round，生成对应 `.piko/summaries/worker_<RoundID>.md`。
- 每完成一个 stage，生成 `.piko/summaries/worker_<StageID>.md`。
- 所有 stage 完成后，生成 `.piko/summaries/worker_storytelling_content_batch.md`。
- 允许一次连续执行 STORY-0 到 STORY-4，但不能跳过任何 round。
- 执行过程中要自己运行每个 round 要求的验证。
- 最终把 `.piko/round_status.json` 更新为：
  - `current_round=STORY-4`
  - `worker_status=ready_for_verify`
  - `verification_status=not_started`
  - `last_completed_round=STORY-4-R02`
  - `worker_summary_file=.piko/summaries/worker_storytelling_content_batch.md`
  - `next_round=null`

必须保持的边界：

- 不发布到公众号、小红书、抖音或任何平台。
- 不上传视频。
- 不克隆或冒充真人声音。
- 不使用未经许可外部图片。
- 不泄露 secrets、API keys、authorization headers。
- 不把草稿标记为已发布。
- 不自动替换 active storytelling template。

最终输出格式：

- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
