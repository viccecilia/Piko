# Storyboard

Format: 9:16, 60 seconds, Chinese knowledge short video.

| Time | Scene | Visual | Voiceover | Screen text |
| --- | --- | --- | --- | --- |
| 0-4s | Hook | Piko pipeline split by adapter gate | 别急着给 Piko 接入新的 Agent 框架。先加一道适配器边界。 | 先加边界，再接框架 |
| 4-10s | Old pain | Split screen: empty research vs unsafe runtime | 以前研究这些框架，很容易走偏。要么能力进不了系统，要么规则被绕开。 | 两个坑：空调研 / 乱接入 |
| 10-17s | New ability | AgentRuntimeAdapter between frameworks and Piko | 今天选的是 AgentRuntimeAdapter boundary。 | AgentRuntimeAdapter |
| 17-32s | Mechanism | Five contract cards | 它有五个 contract：run_task、tool_policy、state_contract、evidence_contract、verification_contract。 | 五个 contract |
| 32-42s | Steps | Five-step rail | 先列框架，再抽接口，做离线 fixture，跑 contract tests，最后交给 CAP。 | 先 fixture，再 tests |
| 42-52s | Limits | Three red gate chips | 重点确认三件事：不默认调用外部 API，不绕过 verify，不自动发布。 | 三个不可绕过 |
| 52-60s | Close | Adapter gate holds, frameworks connected safely | Piko 真正要学的，不是某个框架 API，而是同一套边界。 | 学边界，不是追热点 |

