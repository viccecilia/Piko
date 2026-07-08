# Skill Storytelling And Daily Video Queue

Method: Stage-batch file queue workflow.

Purpose:

Turn Piko's daily skill/agent/capability discoveries into repeatable Chinese content packages: WeChat article, Xiaohongshu carousel, voiceover script, narration plan, storyboard, and local HTML video draft. The default structure is fixed by the `agent-skill-storytelling` skill. Better article structures discovered later must be stored as candidate templates, discussed, versioned, and verified before replacing the active template.

Stage labels:

- STORY-0 Fixed Storytelling Skill Baseline
- STORY-1 Daily Candidate Selection
- STORY-2 Article And Social Copy Generation
- STORY-3 Voiceover And Video Draft Generation
- STORY-4 Verification, History, And Template Evolution

Execution order:

```text
STORY-0-R01 -> STORY-0-R02
STORY-1-R01 -> STORY-1-R02
STORY-2-R01 -> STORY-2-R02 -> STORY-2-R03
STORY-3-R01 -> STORY-3-R02 -> STORY-3-R03
STORY-4-R01 -> STORY-4-R02
```

Relationship to CAP/OSS:

- CAP creates and updates the capability map.
- OSS discovers useful open-source agents, skills, frameworks, and upgrade ideas.
- STORY turns selected capability discoveries into public-facing draft content packages and video drafts.

Global guardrails:

- Do not auto-publish to WeChat, Xiaohongshu, Douyin, or any platform.
- Do not upload generated videos or images to any platform.
- Do not clone or impersonate a real person's voice.
- Do not use external copyrighted images without permission.
- Do not expose secrets, credentials, private local files, API keys, or authorization headers.
- Do not claim a skill/tool can do something not supported by evidence.
- Do not change the active storytelling structure unless a dedicated template evolution round passes verification.
- Generated articles and videos are drafts unless explicitly verified.

Fixed default structure:

```text
强标题 -> 旧痛点 -> 新能力 -> 快速判断
-> 机制解释 -> 实操步骤 -> 真实限制
-> 适合谁 -> 总结和行动
```

Required final verification:

- Skill validation for `agent-skill-storytelling`.
- Artifact existence checks for copy package, storyboard, voiceover, and HTML video draft.
- HTML/video draft sanity probe.
- Guardrail scan for platform publishing, voice cloning, copyrighted image use, secrets, unsupported claims, and template drift.
