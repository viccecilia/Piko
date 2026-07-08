# Round ID: STORY-4-R01

Round Name: Content Package Verification And Guardrails

本轮目标:

对今日图文和视频草稿做最终安全验证，确保可以交给人工审核，而不是自动发布。

本轮任务:
- 执行任务:
  - 检查 latest copy package、voiceover、storyboard、video draft 是否存在。
  - 检查所有 artifact 都保留 draft/internal 状态。
  - 检查 claims 是否有 source_refs 或明确标记为推断。
  - 检查风险说明是否保留。
- 测试任务:
  - 扫描 publish/upload/deploy/voice clone/secrets/API key/authorization/raw copied article 等风险词。
  - 验证 `publish_ready=false`。
  - 验证没有 platform upload action。
- 协作验收任务:
  - 生成 `.piko/summaries/worker_STORY-4-R01.md`。

允许修改:

- `artifacts/storytelling/*`
- `.piko/summaries/worker_STORY-4-R01.md`
- `.piko/round_status.json`

禁止修改:

- 不要把任何 artifact 改成 published。
- 不要绕过人工最终确认。

必须运行的验证:

- Storytelling package guardrail scan。

完成定义:

- 今日内容包通过安全检查，仍处于 draft 状态。

输出格式:
- 修改了什么
- 每个任务状态
- 验证结果
- 协作验收结果
- 未完成/风险
- 下一轮建议
