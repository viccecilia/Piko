# Piko-verify Task: Verify STORY-0 To STORY-4 Batch

请验证 Skill Storytelling And Daily Video Queue 是否完成。

验证范围：

- STORY-0 Fixed Storytelling Skill Baseline
- STORY-1 Daily Candidate Selection
- STORY-2 Article And Social Copy Generation
- STORY-3 Voiceover And Video Draft Generation
- STORY-4 Verification, History, And Template Evolution

必须检查：

- `STORY-INDEX.md` 和所有 STORY round 文件存在。
- `.piko/summaries/worker_STORY-0-R01.md` 到 `.piko/summaries/worker_STORY-4-R02.md` 存在。
- `.piko/summaries/worker_STORY-0.md` 到 `.piko/summaries/worker_STORY-4.md` 存在。
- `.piko/summaries/worker_storytelling_content_batch.md` 存在。
- `artifacts/storytelling/template_registry.json` 存在且 active template 只有 `agent-skill-storytelling:v1`。
- `artifacts/storytelling/latest_candidate_selection.json` 存在。
- `artifacts/storytelling/latest_copy_package.json` 存在且 `publish_ready=false`。
- `artifacts/storytelling/latest_wechat_article.md` 存在。
- `artifacts/storytelling/latest_xiaohongshu.md` 存在。
- `artifacts/storytelling/latest_voiceover.md` 存在。
- `artifacts/storytelling/latest_tts_plan.json` 存在且没有 voice cloning/impersonation。
- `artifacts/storytelling/latest_storyboard.md` 存在。
- `artifacts/storytelling/latest_video/index.html` 存在。

必须运行的验证：

- `python C:\Users\pangv\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\pangv\.codex\skills\agent-skill-storytelling`
- JSON parse probes for:
  - `artifacts/storytelling/template_registry.json`
  - `artifacts/storytelling/latest_candidate_selection.json`
  - `artifacts/storytelling/latest_copy_package.json`
  - `artifacts/storytelling/latest_tts_plan.json`
- HTML existence probe for `artifacts/storytelling/latest_video/index.html`
- Guardrail scan for publish/upload/deploy/voice clone/impersonation/secrets/API key/authorization/raw copied article.

通过条件：

- 所有 STORY stages 和 rounds 完成。
- 所有必需 artifacts 存在。
- active template 未被自动替换。
- 内容包仍是 draft/internal，未发布未上传。
- 未发现 voice cloning、版权图片滥用、secrets、未证实能力夸大。

失败条件：

- 缺少任一必需 summary 或 artifact。
- copy package 被标记为已发布或 publish_ready=true。
- 发生平台发布/上传/部署。
- active template 被未授权替换。
- 使用或声称克隆具体真人声线。
- 保存或复制外部文章长文。
- 发现 secrets/API keys/authorization headers。

验证输出：

- 生成 `.piko/summaries/verify_storytelling_content_batch.md`
- 更新 `.piko/round_status.json`
  - 通过时：`worker_status=complete`、`verification_status=passed`、`last_verified_round=storytelling-content-batch`、`next_round=null`
  - 不通过时：`worker_status=needs_fix`、`verification_status=failed`、`next_round=STORY-<failed-stage-or-round>`

输出格式：

- 验证结论
- 已运行验证
- Stage 完整性检查
- Artifact 检查
- Guardrail 检查
- 发现的问题
- 建议返工任务
